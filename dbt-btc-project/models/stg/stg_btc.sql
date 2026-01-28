{{config(
    materialized = 'incremental',
    incremental_strategy = 'merge',
    unique_key = 'HASH_KEY'
)}}


with BTC as (

select
*
from {{source('src_btc','btc')}}
qualify row_number() over (partition by hash_key order by block_number desc) = 1 -- Filter for the more recent block number so we have one entry per Hash Key
 
)

select
*
from BTC 

{% if is_incremental() %}

where BLOCK_TIMESTAMP >= (select max(BLOCK_TIMESTAMP) from {{ this }} )

{% endif %}