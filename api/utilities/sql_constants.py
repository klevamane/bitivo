"""Module that holds re-useable sql queries"""


def last_stock(extra_filter=''):
    return \
        f"""
    last_stock AS (SELECT max(stcnt.stock_date) as stock_date, stcnt.stcnt_ac_id as asset_category_id from
    (SELECT stock_counts.created_at AS stock_date, stock_counts.asset_category_id as stcnt_ac_id
    FROM stock_counts  WHERE stock_counts.deleted = False {extra_filter}) as stcnt group by stcnt.stcnt_ac_id)

    """


# sql to get list of asset categories with stats from CTE
SELECT_CATEGORIES_WITH_STATS = \
    """
    SELECT * FROM categories_with_stats WHERE id IS NOT NULL AND parent_id IS NULL {filter} ORDER BY {sort} {order}
    LIMIT :limit OFFSET :offset
    """
ASSET_CATEGORIES_WITH_STATS_CTE = \
    """
     WITH categories AS (SELECT ac.id,ac.name,ac.priority,ac.running_low, ac.parent_id,
    ac.created_at,ac.updated_at,ac.deleted,ac.deleted_at,ac.created_by,ac.updated_by,ac.deleted_by,ac.low_in_stock,ac.image::jsonb,
    count(a.id) AS assets_count
    FROM asset_categories ac LEFT JOIN  asset a ON ac.id = a.asset_category_id
    AND a.deleted = false
    WHERE ac.deleted = false GROUP BY ac.id),

    total_ok_assets AS (SELECT count(asset.id) AS total_ok_assets, asset.asset_category_id FROM asset
    WHERE asset.deleted = false  AND asset.center_id IS NOT NULL AND asset.status
    IN {ok_status}
    GROUP BY asset.asset_category_id),

    assets_assigned_to_spaces AS (SELECT count(asset.assignee_type) AS space_assignee, asset_category_id
    FROM asset WHERE asset.assignee_type = 'space' AND asset.deleted = False  AND asset.center_id IS NOT NULL
    AND asset.status IN {ok_status}
    GROUP BY asset.asset_category_id),

    assets_assigned_to_users AS (SELECT count(asset.assignee_type) AS people_assignee, asset_category_id
    FROM asset WHERE asset.assignee_type = 'user'  AND asset.deleted = False  AND asset.center_id IS NOT NULL 
    AND  asset.status IN {ok_status}
    GROUP BY asset.asset_category_id),

    {LAST_STOCK},

    last_stock_count AS (SELECT stock_counts.count AS last_stock_count, stock_date, stock_counts.asset_category_id
    FROM stock_counts JOIN last_stock ON stock_counts.created_at = last_stock.stock_date
    WHERE stock_counts.deleted = False AND stock_counts.center_id IS NOT NULL AND stock_counts.asset_category_id = last_stock.asset_category_id),

    categories_with_stats AS (SELECT c.*,
    COALESCE(total_ok_assets,0) AS total_ok_assets, COALESCE(space_assignee,0) AS space_assignee,
    COALESCE(people_assignee, 0) AS people_assignee, COALESCE(last_stock_count, 0) AS last_stock_count, stock_date
    FROM categories c LEFT JOIN  total_ok_assets ON c.id = total_ok_assets.asset_category_id
    LEFT JOIN  assets_assigned_to_spaces aas ON c.id = aas.asset_category_id
    LEFT JOIN  assets_assigned_to_users aau ON c.id = aau.asset_category_id
    LEFT JOIN  last_stock_count ON c.id = last_stock_count.asset_category_id)

    {select}
    """
date_filter = "AND stock_counts.created_at between {startDate} and {endDate}"
LAST_STOCK = last_stock()

LAST_STOCK_WITH_DATE = last_stock(extra_filter=date_filter)

# sql to get list of asset categories with custom attributes and  stats from CTE
SELECT_CATEGORIES_WITH_ATTRIBUTES_AND_STATS = \
    """

    ,attributes_and_stats AS (SELECT cws.*,
    JSON_AGG(JSON_BUILD_OBJECT('id', at.id, 'key', at._key, 'label', at.label, 'inputControl', at.input_control , 'isRequired', at.is_required ))
    AS "customAttributes" FROM categories_with_stats cws LEFT JOIN attribute at
    ON cws.id = at.asset_category_id GROUP BY cws.name, cws.id, cws.assets_count, cws.priority, cws.running_low, cws.low_in_stock, cws.total_ok_assets, cws.parent_id,
    cws.space_assignee, cws.people_assignee, cws.last_stock_count, cws.stock_date, cws.created_at, cws.deleted, cws.updated_at, cws.deleted_at, cws.created_by,
    cws.updated_by, cws.deleted_by,cws.image::jsonb)

    SELECT * FROM attributes_and_stats WHERE id IS NOT NULL {filter} ORDER BY {sort} {order} LIMIT :limit OFFSET :offset
    """
# sql to get a single asset category with stats from CTE
SELECT_CATEGORY_STATS = "SELECT * FROM categories_with_stats cws WHERE cws.id = :cat_id"

start = "(select min(stock_counts.created_at) from stock_counts)"
end = "(select max(stock_counts.created_at) from stock_counts)"


EXISTS = \
    """
    SELECT 1
    FROM {table}
    WHERE {table}.{column} = '{value}'
    AND {table}.deleted = false
    """
