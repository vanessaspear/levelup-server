SELECT * FROM levelupapi_gametype;

SELECT * FROM auth_user;
SELECT * FROM authtoken_token;
SELECT * FROM levelupapi_gamer;

DELETE FROM levelupapi_game
WHERE id = 7;


SELECT g.*, u.first_name || " " || u.last_name AS 'Gamer Name', gr.id AS 'Gamer ID'
FROM levelupapi_game g 
JOIN levelupapi_gamer gr
    ON gr.id = g.gamer_id
JOIN auth_user u
    ON u.id = gr.user_id; 


SELECT e.id, e.datetime, g.title, u.first_name || " " || u.last_name AS 'full_name', gr.id AS 'gamer_id'
FROM levelupapi_event e 
JOIN levelupapi_game g
    ON g.id = e.game_id
JOIN levelupapi_gamer gr
    ON gr.id = e.gamer_id
JOIN auth_user u
    ON u.id = gr.user_id;