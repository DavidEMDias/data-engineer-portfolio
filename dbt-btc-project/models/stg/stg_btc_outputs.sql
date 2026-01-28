{{ config(
    materialized = 'incremental',
    incremental_strategy = 'append'
) }}

WITH max_existing AS (
    SELECT MAX(block_timestamp) AS max_ts
    FROM {{ this }}
),

flattened_outputs AS (
    SELECT 
        tx.hash_key,
        tx.block_number,
        tx.block_timestamp,
        tx.is_coinbase,
        f.value:address::STRING AS output_address,
        f.value:value::FLOAT AS output_value
    FROM {{ ref("stg_btc") }} tx,
         LATERAL FLATTEN(input => outputs) f
    WHERE f.value:address IS NOT NULL

    {% if is_incremental() %}
      AND tx.block_timestamp >= (SELECT max_ts FROM max_existing)
    {% endif %}
)

SELECT 
    hash_key,
    block_number,
    block_timestamp,
    is_coinbase,
    output_address,
    output_value
FROM flattened_outputs

