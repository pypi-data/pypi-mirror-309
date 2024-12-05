from typing import Final


# ====== CFn: Common Custom Function ======
class CFn:
    schema: Final[str] = 'cfn'
    array_sort: Final[str] = f'{schema}.array_sort'
    array_sort_unique: Final[str] = f'{schema}.array_sort_unique'

    bigint_2_id: Final[str] = f'{schema}.bigint_2_id'
    bigint_array_2_id_array: Final[str] = f'{schema}.bigint_array_2_id_array'

    count_jsonb_keys: Final[str] = f'{schema}.count_jsonb_keys'

    http_status_data: Final[str] = f'{schema}.http_status_data'
    http_status_error: Final[str] = f'{schema}.http_status_error'
    http_status_error_code_only: Final[str] = f'{schema}.http_status_error_code_only'

    id_2_bigint: Final[str] = f'{schema}.id_2_bigint'
    id_2_int: Final[str] = f'{schema}.id_2_int'
    if_null_2_empty_bigint_array: Final[str] = f'{schema}.if_null_2_empty_bigint_array'
    if_null_2_empty_uuid_array: Final[str] = f'{schema}.if_null_2_empty_uuid_array'
    int_2_id: Final[str] = f'{schema}.int_2_id'
    is_null: Final[str] = f'{schema}.is_null'

    jsonb_add_key_value_elements: Final[str] = f'{schema}.jsonb_add_key_value_elements'
    jsonb_array_2_bigint_array: Final[str] = f'{schema}.jsonb_array_2_bigint_array'
    jsonb_array_2_int_array: Final[str] = f'{schema}.jsonb_array_2_int_array'
    jsonb_2_jsonb_array: Final[str] = f'{schema}.jsonb_2_jsonb_array'
    jsonb_array_2_smallint_array: Final[str] = f'{schema}.jsonb_array_2_smallint_array'
    jsonb_array_2_text_array: Final[str] = f'{schema}.jsonb_array_2_text_array'
    jsonb_array_2_lower_text_array: Final[str] = f'{schema}.jsonb_array_2_lower_text_array'
    jsonb_array_2_uuid_array: Final[str] = f'{schema}.jsonb_array_2_uuid_array'
    jsonb_remove_key: Final[str] = f'{schema}.jsonb_remove_key'

    jsonb_id_array_2_bigint_array: Final[str] = f'{schema}.jsonb_id_array_2_bigint_array'
    jsonb_id_array_2_int_array: Final[str] = f'{schema}.jsonb_id_array_2_int_array'

    is_text_in_array: Final[str] = f'{schema}.is_text_in_array'

