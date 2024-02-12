"""
Module for raw SQL queries
"""

from ..utilities.enums import AssetStatus
from ..utilities.sql_constants import \
    ASSET_CATEGORIES_WITH_STATS_CTE, LAST_STOCK, LAST_STOCK_WITH_DATE,\
    SELECT_CATEGORIES_WITH_STATS, SELECT_CATEGORIES_WITH_ATTRIBUTES_AND_STATS,\
    SELECT_CATEGORY_STATS

ok_status = AssetStatus.get_ok_status()
get_reconciliation_status = AssetStatus.get_reconciliation_status()

# CTE implementation to get asset categories with stats
"""
ALIAS USED IN THIS CTE
a     asset
aas   assets_assigned_to_spaces
aau   assets_assigned_to_users
ac    asset categories
at    attributes
c     categories
cws   categories_with_stats
stcnt = stock_count
"""

sql_queries = {
    'get_column': 'SELECT {} FROM {}',
    'check_user_permissions':
    '''\
    SELECT users.name AS user_name, roles.title AS role_title, permissions.type AS permission_type, resources.name AS resource_name
    FROM users
    JOIN roles ON roles.id = users.role_id
    JOIN resource_access_levels ON resource_access_levels.role_id = roles.id
    JOIN resource_permissions ON resource_permissions.resource_access_level_id = resource_access_levels.id
    JOIN permissions ON permissions.id = resource_permissions.permission_id
    JOIN resources ON resources.id = resource_access_levels.resource_id
    WHERE users.token_id = '{0}' AND users.deleted=False  AND resources.name = '{1}' AND permissions.type != '{2}' AND (permissions.type = '{3}' OR permissions.type = '{4}')
    ''',
    'check_asset_category_levels':
    '''
    SELECT name, running_low,low_in_stock, COUNT(asset.id) AS available_assets FROM asset_categories
    LEFT JOIN asset ON asset.asset_category_id = asset_categories.id AND asset.status IN ('{0}', '{1}', '{2}') AND asset.deleted = False
    WHERE asset_categories.deleted = False GROUP BY asset_categories.id
    ''',
    'unreconciled_asset':
        ASSET_CATEGORIES_WITH_STATS_CTE
        .format(ok_status=ok_status, LAST_STOCK=LAST_STOCK_WITH_DATE, select=SELECT_CATEGORIES_WITH_STATS),

    'categories_with_stats':
    ASSET_CATEGORIES_WITH_STATS_CTE
        .format(ok_status=ok_status, LAST_STOCK=LAST_STOCK, select=SELECT_CATEGORIES_WITH_STATS),
    'attributes_and_stats':
    ASSET_CATEGORIES_WITH_STATS_CTE
        .format(ok_status=ok_status, LAST_STOCK=LAST_STOCK, select=SELECT_CATEGORIES_WITH_ATTRIBUTES_AND_STATS),
    'single_category_stats': ASSET_CATEGORIES_WITH_STATS_CTE
        .format(ok_status=ok_status, LAST_STOCK=LAST_STOCK, select=SELECT_CATEGORY_STATS),
    'asset_categories_count': 'SELECT COUNT(*) FROM asset_categories ac WHERE ac.deleted=FALSE AND ac.parent_id IS NULL',
    'get_total_reconciliation':
    '''
    WITH category AS (SELECT DISTINCT asset_categories.name, asset_categories.id, stock_counts.count FROM asset_categories
    JOIN asset ON asset.asset_category_id = asset_categories.id
    JOIN stock_counts ON stock_counts.asset_category_id = asset_categories.id
    WHERE asset.deleted = False AND asset.center_id IS NOT NULL AND asset_categories.deleted=False AND stock_counts.created_at BETWEEN '{0}' AND '{1}'),

    ok_asset_expected_store_count AS (select COUNT(asset.id) AS ok_asset_expected_store_count FROM asset
    JOIN category ON category.id = asset.asset_category_id AND asset.deleted = False ''' + f'''
    AND asset.assignee_type = 'store' AND asset.status IN {get_reconciliation_status})

    SELECT COUNT(distinct id) FROM category, ok_asset_expected_store_count WHERE ok_asset_expected_store_count != category.count;
    ''',
    'get_asset_flow_count':
    '''
    WITH inflow AS (SELECT COUNT(id) AS inflow
    FROM asset WHERE asset.deleted = False AND asset.assignee_type = 'store'
    AND asset.date_assigned BETWEEN '{0}' AND '{1}'), outflow AS (select COUNT(id) AS outflow
    FROM asset
    WHERE asset.deleted = False AND asset.assignee_type != 'store'
    AND asset.date_assigned BETWEEN '{0}' AND '{1}')
    SELECT * FROM inflow, outflow
    ''',
    'get_summary_request':
    '''
    select count(id) as totalRequest,
    sum(case when status = 'open' then 1 else 0 end) as totalOpenRequests,
    sum(case when status='in_progress' then 1 else 0 end) as totalInProgressRequests,
    sum(case when status = 'completed' then 1 else 0 end) as totalCompletedRequests,
    sum(case when status = 'closed' then 1 else 0 end) as totalClosedRequests,
    sum(case when due_by < now() and (status='open' or status='in_progress') then 1 else 0 end) as totalOverdueRequests
    from  requests
    {}
    ''',
    'get_due_schedules':
    '''
    SELECT users.name, users.email,
    JSON_AGG(work_orders.title) AS title FROM users
    JOIN schedules ON users.token_id = schedules.assignee_id
    JOIN work_orders ON schedules.work_order_id = work_orders.id
    WHERE schedules.due_date::DATE = CURRENT_DATE and schedules.status = 'pending'
    GROUP by users.name, users.email
    ''',
    'get_incidence_report':
    '''
    select
    sum(case when r.status = 'open' and r.due_by >= now() then 1 else 0 end) as totalOpenRequests,
    sum(case when r.status='in_progress' then 1 else 0 end) as totalInProgressRequests,
    sum(case when r.status = 'completed' then 1 else 0 end) as totalCompletedRequests,
    sum(case when r.status = 'closed' then 1 else 0 end) as totalClosedRequests,
    sum(case when r.due_by < now() and (r.status='open' or r.status='in_progress') then 1 else 0 end) 
    as totalOverdueRequest, rt.title
    from  requests r
    inner join request_types rt
    on rt.id = r.request_type_id
    WHERE r.center_id IS NOT NULL
    GROUP BY rt.title
    ''',
    'get_hot_desks_of_users':
    '''
    SELECT MAX(hot.created_at)
    AS created_at, count(*),
    (SELECT hot_desk_ref_no FROM hot_desk_requests WHERE created_at = MAX(hot.created_at) LIMIT 1),
    (SELECT requester_id FROM hot_desk_requests WHERE created_at = MAX(hot.created_at) LIMIT 1),
    (SELECT assignee_id FROM hot_desk_requests WHERE created_at = MAX(hot.created_at) LIMIT 1)
    FROM hot_desk_requests AS hot WHERE status='{0}' AND \
    deleted=FALSE AND created_at BETWEEN '{1}' AND '{2}'
    group by requester_id
    ''',
    'trends_allocation':
    '''
    SELECT
    date_part('{0}', created_at::date) AS {1},
    sum(case when hot_desk_requests.status = 'approved' then 1 else 0 end) as sum  
    FROM hot_desk_requests
    WHERE hot_desk_ref_no LIKE '{2}%'
    AND created_at between '{3}' and '{4}'
    GROUP BY {1}
    ORDER BY {1}
    ''',
    'get_building_spaces':
    '''
    WITH RECURSIVE CTE AS (
    SELECT * from spaces where spaces.id='{}'
    UNION ALL
    SELECT spaces.*
    from CTE c
    JOIN spaces
    on spaces.parent_id=c.id)
    SELECT CTE.id,name,parent_id as "parentId",space_type_id as "spaceTypeId", type, color, center_id as "centerId" from CTE JOIN space_types ON space_type_id=space_types.id WHERE CTE.deleted=FALSE
    ''',
    'get_space_types':
    '''
    SELECT id, type, color from space_types
    ''',
    'get_cancellation_reasons_count':
    '''
    SELECT
    COUNT(CASE WHEN reason = 'changed my mind' THEN 1 END) AS change_my_mind_count,
    COUNT(CASE WHEN reason ='leaving early' THEN 1 END) AS leaving_early_count,
    COUNT(CASE WHEN reason = 'delayed approval' THEN 1 END) AS delayed_approval_count,
    COUNT(CASE WHEN reason = 'seat changed' THEN 1 END) AS seat_changed_count,
    COUNT(CASE WHEN (reason !='changed my mind' and reason !='leaving early' and reason !='delayed approval' and reason !='seat changed') THEN 1 END)\
    AS other_count
    FROM  hot_desk_requests
    WHERE status ='cancelled'
    AND created_at between '{0}' AND '{1}'
    ''',
    'hotdesk_responder_counts':
    '''
    SELECT
    COUNT(CASE WHEN status='approved' and (is_escalated is not True) THEN 1 ELSE NULL END
    ) as approvals_count,
    COUNT(CASE WHEN status='rejected' and (is_escalated is not True) THEN 1 ELSE NULL END
    ) as rejections_count,
    COUNT(CASE WHEN (status='pending' and created_at < '{0}') or is_escalated THEN 1 ELSE NULL END
    ) as missed_count,
    assignee_id
    FROM hot_desk_responses where created_at between '{1}' and '{2}'
    GROUP BY assignee_id
    ''',
    'trends_allocation_of_user':
    '''
    SELECT
    date_part('{0}', created_at::date) AS {1},
    sum(case when hot_desk_requests.requester_id = '{2}' then 1 else 0 end) AS sum
    FROM hot_desk_requests
    WHERE hot_desk_ref_no LIKE '{3}%'
    AND status='approved'
    AND created_at between '{4}' and '{5}'
    GROUP BY {1}
    ORDER BY {1}
    ''',
    'get_asset_category_subcategories':
    '''
    WITH RECURSIVE CTE AS (
    SELECT * FROM asset_categories
    WHERE asset_categories.id = '{}'
    UNION ALL
    SELECT ac.* from CTE
    JOIN asset_categories ac ON ac.parent_id = CTE.id)
    SELECT ac.* from CTE c JOIN asset_categories ac ON ac.parent_id = c.id
    ''',
}
