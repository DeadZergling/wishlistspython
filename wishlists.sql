SELECT * FROM wishlists.users;

SELECT * FROM wishlists.items;

SELECT * FROM users_has_items;

# Get users wish list:

SELECT items.name as item_name, items.id as item_id, users.name as added_by_name, users.id as added_by_id, items.created_at as date_added FROM users
LEFT JOIN users_has_items ON users_has_items.user_id = users.id
LEFT JOIN items ON users_has_items.item_id = items.id
WHERE users.id = 1 and items.name is not null;

# Get users not wish list:

SELECT items.name as item_name, items.id as item_id, users.name as added_by_name, users.id as added_by_id, items.created_at as date_added FROM users
LEFT JOIN items ON users.id = items.user_id WHERE items.name is not null AND NOT item_id IN(SELECT items.id as item_id FROM users
LEFT JOIN users_has_items ON users_has_items.user_id = users.id
LEFT JOIN items ON users_has_items.item_id = items.id
WHERE users.id = 1 and items.name is not null);

SELECT items.name as item_name, items.id as item_id, users.name as added_by_name, users.id as added_by_id, items.created_at as date_added FROM users
LEFT JOIN items ON users.id = items.user_id WHERE items.name is not null AND NOT items.id IN(SELECT items.id FROM users
LEFT JOIN users_has_items ON users_has_items.user_id = users.id
LEFT JOIN items ON users_has_items.item_id = items.id
WHERE users.id = 2 and items.name is not null);

SELECT items.id as item_id FROM users
LEFT JOIN users_has_items ON users_has_items.user_id = users.id
LEFT JOIN items ON users_has_items.item_id = items.id
WHERE users.id = 1;

SELECT users.username, users.password FROM users;