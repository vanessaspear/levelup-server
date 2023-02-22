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