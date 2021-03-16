-------------------------
-------------------------
-- SECCIÓN 2
-------------------------
-------------------------

------------------------
-- SELECT

	-- Selecciona uno o varios elementos de una tabla
select value 
from table;

select *
from payment;

select customer_id, amount
from payment

-------------------------
-- SELECT distinct 

	-- Selecciona los valores unicos de una o varias columnas
select distinct column_1, column_2
from table;

-------------------------
-- select where

	-- Selecciona elementos dado una condición ( = , < , > , <= , >=, != , AND, OR )
select column_2
from table_1
where column_2 = 1

-------------------------
-- COUNT

	-- Esta función regresa una cierta cantidad de registros que cumplen con una condición
select count(column_1)
from table_1;

select count (distinct amount)
from payment;


-------------------------
-- Limit

	-- Límite el número de registros mostrados
select column_1
from table_1
limit 10;

-------------------------
--
-- Order by

	-- Obten el customer ID para las 10 cantidades mayor pagadas
select customer_id, amount
from payment
order by amount desc
limit 10;

	-- Obten el ID de las películas cuyo ID este entre 1 y 5
select film_id, title
from film
order by film_id
limit 5;

-------------------------
-- Between

	-- Usa el operador between para hacer coincidir un valor contra un rango de valores
		where value between low and high;
	
select customer_id, amount
from payment
where amount between 8 and 9;

select amount, payment_date
from payment
where payment_date between '2007-02-07' and '2007-02-15';

-------------------------

-- IN

	-- Se usa el operador IN junto con WHERE para obtener aquellos registros  
	-- que coinciden con uno o más valores dados, es una simplificada de usar la función OR
		
value IN (value1, value2,...)

	-- El siguiente query obtiene las columnas solicitadas en donde el customer_id
	-- contiene los valores 7,13,10
	
select customer_id, rental_id, return_date
from rental
where customer_id in (7,13,10)
order by return_date desc;

	-- Obtenemos todos los registros en donde el amount es igual a 7.99 y 8.99
select *
from payment
where amount in (7.99, 8.99);

-------------------------

-- Like - ilike

	-- Encuentra un elemento en donde tenga cierta coincidencia con una condición
	-- Like es sensible mayusculas/minusculas
	-- ilike no es sensible a mayusculas/minusculas
	-- 'X%' Empieza con X caracteres, pattern matching
	-- '%X' Termina con X caracteres
	-- '%X%' Contiene X caracteres dentro de su valor
	-- '_' Remplaza el guión bajo por cualquier valor, "comodín"
	
select first_name
from customer
where first_name like 'Jen%' -- Encuentra valores que empiecen con Jen

select first_name
from customer
where first_name like '%y' -- Encuentra valores que terminen con y

select first_name
from customer
where first_name like '%er%' -- Encuentra valores que contengan er en alguna parte 

select first_name
from customer
where first_name like '_her%' -- Remplaza _ con cualquier valor y después cumple la codición
			                  -- del %

-------------------------

-- CHALLENGE
-- ¿ Cuántas transacciones fueron superiores a $5.00 ? 
	-- 3618 transacciones

select count(amount)
from payment
where amount > 5;

-- ¿ Cuántos actores tienen un first_name que empiece con la letra P ?
-- 5 actores
select count(*)
from actor
where first_name like 'P%';

-- ¿ De cuántos distritos unicos son nuestros clientes?
-- 378 distritos

select count(distinct (district))
from address;

-- Del query anterior recupera la lista de distritos unicos 

select distinct (district)
from address;

-- ¿Cuántos clientes hay por cada distrito de la lista anterior?

select district, count (*)
from address
group by district
order by count(*) desc;

-- ¿ Cuántos fims tienen un rating de R y un replacement cost de entre $5 y $15?
-- 52 films

select count(*)
from film
where rating = 'R' and replacement_cost between 5 and 15;

-- ¿ Cuántos films contienen la palabra Truman en alguna parte de su nombre?
-- 5 films

select count(*)
from film
where title like '%Truman%';

-------------------------
-------------------------
-- SECCIÓN 3
-------------------------
-------------------------

-- MIN MAX AVG SUM funciones de agregación
	-- Combinan los valores en un solo valor, dado la función de agregación

	-- AVG Promedio
select avg (amount)
from payment;

select round (avg (amount), 2) -- round redondea la cantidad de decimales al número indicado
from payment;

	-- MIN
select min (amount)
from payment;

	-- MAX
select max (amount)
from payment;

	-- SUM
select sum (amount)
from payment;

-- Group by
	-- Agrupa por valores unicos
	-- Divide el número de registros obtenidos en grupos, para cada grupo 
	-- puedes usar una función de agregación
	
select column_1, aggregate_function(column_2)
from table_1
group by column_1

	-- Agrupa los valores unicos de una columna, similar a DISTINCT
select customer_id
from payment
group by customer_id;

	-- Agrupa los valores unicos de la columna costumer_id, y suma los valores de amount de acuerdo al customer_id
select customer_id, sum(amount)
from payment
group by customer_id;

	-- Para cada customer_id obtiene los valores MIN, AVG, MAX y SUM de la columna amount
select customer_id, min (amount), round(avg (amount),2), max (amount), sum(amount)
from payment
group by customer_id;

	-- Agrupa el staff_id y cuenta el número de filas que hay en cada uno de estos grupos
select staff_id, count(*)
from payment
group by staff_id;

-------------------------
-------------------------
-- CHALLENGE
-------------------------
-------------------------

-- ¿Cuántos pagos ha procesado cada uno de los miembros del staff? y ¿cuál ha sido la cantidad de dichos pagos?

select staff_id, count (*), sum (amount)
from payment
group by staff_id;

-- ¿Cuál es el replacement cost promedio de las peliculas de acuerdo a su rating?

select rating, round(avg(replacement_cost),2)
from film
group by rating;

-- ¿Cuáles son los 5 customer_id que más han gastado en nuestra tienda?

select customer_id, sum (amount)
from payment
group by customer_id
order by sum (amount) desc
limit 5;

-------------------------
-- HAVING
	--Se usa HAVING junto a group by para filtrar registros que no cumplan con cierta condición
	-- Having establece una condición para los registros creados por group by, mientras que where establece la condición
		-- los registros individuales, antes de que group by se aplique
select column_1 aggregate_function (column_2)
from table_name
group by column_1
having condition;

	-- agrupa por customer_id y da la suma del amount de cada ID, de eso hace un filtro para 
		--solo mostrar los id con un sum amount superior a 200
select customer_id, sum (amount)
from payment
group by customer_id
having sum(amount) > 200

	-- agrupa por store_id, hace un count de los customer_id para cada store, y regresa solo aquellos 
		-- store_id donde el count fue superior a 300
select store_id, count(customer_id)
from customer
group by store_id
having count (customer_id) > 300;

	-- agrupa por rating, pero hace un filtro para solo agrupar los que sean R  G y PG, a esos les saca el promedio
		-- rental_rate y filtra para solo mostrar aquellos que sean inferiores a 3 
select rating, avg(rental_rate)
from film
where rating in ('R', 'G', 'PG')
group by rating
having avg(rental_rate) < 3;

-------------------------
-- CHALLENGE
-------------------------

-- ¿ Qué movie ratings tienen un promedio de rental_duration  mayor a 5 días?

select rating, avg (rental_duration)
from film
group by rating
having avg (rental_duration) > 5;

-------------------------
-------------------------
-- SECCIÓN 4
-------------------------
-------------------------

-------------------------
-- Examen
-------------------------


-- Recupera el customer_id de aquellos clientes que han gastado al menos $110 con el staff memder que tiene un ID = 2

select customer_id, sum (amount)
from payment
where staff_id = 2
group by customer_id
having sum (amount) > 110;

-- ¿Cuántos films empiezan con la letra J ?

select count (*)
from film
where title like 'J%';

-- ¿ Qué cliente tiene el customer_id más grande y qué su nombre empiece con la letra E
--   y tenga un addres_id menor que 500? 

select *
from customer
where first_name like 'E%'and address_id < 500
order by customer_id desc
limit 1;

-------------------------
-------------------------
-- SECCIÓN 5
-------------------------
-------------------------

-------------------------
-- AS
	-- Nos permite renombrar columnas o selecciones de columnas con un alías 

select payment_id as my_payment_column
from payment

select customer_id, sum(amount) as total_spent
from payment
group by customer_id;

-- JOIN
	-- Une los registros de una tabla con otra, dada un condición de igualdad
	-- Varioa tipos de join INNER, OUTER, RIGTH, LEFT

	-- INNER JOIN
	-- Regresa las filas de la tabla A que tengan coincidencias en la tabla B
select  a.pka, a.ci, b.pkb, b.c2
from a
inner join b on a.pka = b.fka

select 
	customer.customer_id, first_name, 
	last_name,	email,
	amount,	payment_date
from customer
inner join payment 
	on payment.customer_id = customer.customer_id
order by customer.customer_id;
	
	-- FULL OUTER JOIN
	-- Regresa todas las filas de ambas tablas, exista o no coincidencia de valores
	
	-- FULL OUTER JOIN with WHERE
	-- Regresa todas las filas de ambas tablas, en los que no hay coincidencia de valores
	
	-- LEFT OUTER JOIN
	-- 	Regresa todas las filas de la tabla A, con las coincidencias de la tabla B
	
	-- LEFT OUTER JOIN with WHERE
	-- Regresa solo los registros que se encuentran presentes en la tabla ABS

select * 
from tableA
left outer join tableB on tableA.name = tableB.name
where tableB.id is null;

select film.film_id, film.title, inventory_id
from film
left outer join inventory on inventory.film_id = film.film_id;

-- UNION
	-- Combina el resultado de dos o más selecciones en uno solo
	-- Ambos querys deben tener el mismo número de columnas
	-- Las columnas correspondientes deben de tener el mismo tipo de dato
	-- UNION remueve los valores duplicados (mismo valor en todas las columnas) a menos que se use UNION ALL
	-- Combinar datos de tablas similares
	
select c1, c2
from t1
union
select c1, c2,
from t2;

-- 
-- TIMESTAMP

-- Extract: extrae un valor de un dato con formato timestamp 
--extract (unit from date)
-- 
-- extrae el día de cada valor de payment_date
select customer_id, extract ( day from payment_date) as day
from payment;

-- Selecciona la suma de amount, extrae el mes de cada payment_date y agrupalo por mes,
-- ordenalo de forma descendente de acuerdo al total y limitalo a 5 registros
-- Da el total de cada mes para los 5 meses con mayor ganancia
select sum(amount) as total, extract (month from payment_date) as month
from payment
group by month
order by total desc
limit 5;


select count(bici) as bicis, extract (month from hora_retiro) as hour
from b
group by hour






































