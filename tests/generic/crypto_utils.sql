 {% test assert_valid_btc_address(model, column_name) %} -- Validate BTC Address
 
    select *
    from {{ model }}
    where NOT (
        {{ column_name }} LIKE '1%' OR
        {{ column_name }} LIKE '3%' OR
        {{ column_name }} LIKE 'bc1%'
    )

{% endtest %}