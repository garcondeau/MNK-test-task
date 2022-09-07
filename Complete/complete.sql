use mnktask;
SELECT 
    main_part_number,
    manufacturer,
    category,
    origin,
    IFNULL(deposit.deposit, 0) AS deposit,
    price.price,
    quantity.quantity,
    quantity.warehouse,
    IFNULL(price + deposit.deposit, price) AS total
FROM
    data
        LEFT JOIN
    deposit ON data.part_number = deposit.part_number
        JOIN
    price ON data.part_number = price.part_number
        JOIN
    quantity ON data.part_number = quantity.part_number
WHERE
    quantity.warehouse = 'A'
        OR quantity.warehouse = 'H'
        OR quantity.warehouse = 'J'
        OR quantity.warehouse = '3'
        OR quantity.warehouse = '9'
        AND (price + deposit.deposit) > 2 
UNION SELECT 
    main_part_number,
    manufacturer,
    category,
    origin,
    IFNULL(deposit.deposit, 0) AS deposit,
    price.price,
    quantity.quantity,
    quantity.warehouse,
    IFNULL(price + deposit.deposit, price) AS total
FROM
    data
        RIGHT JOIN
    deposit ON data.part_number = deposit.part_number
        JOIN
    price ON data.part_number = price.part_number
        JOIN
    quantity ON data.part_number = quantity.part_number
WHERE
    quantity.warehouse = 'A'
        OR quantity.warehouse = 'H'
        OR quantity.warehouse = 'J'
        OR quantity.warehouse = '3'
        OR quantity.warehouse = '9'
        AND (price + deposit.deposit) > 2
