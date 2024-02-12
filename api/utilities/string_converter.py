def snake_case_to_title_case(snake_str):
    """Converts string from snake_case to title case(all first letters capitalized)

    Args:
        (string): the string to be converted
           
    Returns:
        (string): the string converted to title case
    """
    title_str = snake_str.split('_')
    return ' '.join(title_str).title()
