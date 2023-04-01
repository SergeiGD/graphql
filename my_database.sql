--
-- PostgreSQL database dump
--

-- Dumped from database version 12.14 (Ubuntu 12.14-0ubuntu0.20.04.1)
-- Dumped by pg_dump version 12.14 (Ubuntu 12.14-0ubuntu0.20.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: base_order; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.base_order (
    id integer NOT NULL,
    date_created timestamp without time zone NOT NULL,
    type character varying NOT NULL
);


ALTER TABLE public.base_order OWNER TO sergei;

--
-- Name: base_order_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.base_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.base_order_id_seq OWNER TO sergei;

--
-- Name: base_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.base_order_id_seq OWNED BY public.base_order.id;


--
-- Name: cart; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.cart (
    id integer NOT NULL,
    cart_uuid character varying NOT NULL
);


ALTER TABLE public.cart OWNER TO sergei;

--
-- Name: category; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.category (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    price numeric NOT NULL,
    prepayment_percent double precision NOT NULL,
    refund_percent double precision NOT NULL,
    main_photo_path character varying NOT NULL,
    rooms_count integer NOT NULL,
    floors integer NOT NULL,
    beds integer NOT NULL,
    square double precision NOT NULL,
    date_created timestamp without time zone NOT NULL,
    date_deleted timestamp without time zone,
    is_hidden boolean NOT NULL
);


ALTER TABLE public.category OWNER TO sergei;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.category_id_seq OWNER TO sergei;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.category_id_seq OWNED BY public.category.id;


--
-- Name: category_sale; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.category_sale (
    sale_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.category_sale OWNER TO sergei;

--
-- Name: category_tag; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.category_tag (
    tag_id integer NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.category_tag OWNER TO sergei;

--
-- Name: client; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.client (
    id integer NOT NULL,
    date_of_birth date
);


ALTER TABLE public.client OWNER TO sergei;

--
-- Name: client_order; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.client_order (
    id integer NOT NULL,
    comment character varying,
    paid numeric NOT NULL,
    refunded numeric NOT NULL,
    date_full_prepayment timestamp without time zone,
    date_full_paid timestamp without time zone,
    date_finished timestamp without time zone,
    date_canceled timestamp without time zone,
    client_id integer NOT NULL
);


ALTER TABLE public.client_order OWNER TO sergei;

--
-- Name: group; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public."group" (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public."group" OWNER TO sergei;

--
-- Name: group_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.group_id_seq OWNER TO sergei;

--
-- Name: group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.group_id_seq OWNED BY public."group".id;


--
-- Name: group_permission; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.group_permission (
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.group_permission OWNER TO sergei;

--
-- Name: people; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.people (
    id integer NOT NULL,
    first_name character varying,
    last_name character varying,
    email character varying NOT NULL,
    password character varying,
    date_created timestamp without time zone NOT NULL,
    date_deleted timestamp without time zone,
    type character varying NOT NULL
);


ALTER TABLE public.people OWNER TO sergei;

--
-- Name: people_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.people_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.people_id_seq OWNER TO sergei;

--
-- Name: people_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.people_id_seq OWNED BY public.people.id;


--
-- Name: permission; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.permission (
    id integer NOT NULL,
    name character varying NOT NULL,
    code character varying NOT NULL
);


ALTER TABLE public.permission OWNER TO sergei;

--
-- Name: permission_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.permission_id_seq OWNER TO sergei;

--
-- Name: permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.permission_id_seq OWNED BY public.permission.id;


--
-- Name: photo; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.photo (
    id integer NOT NULL,
    "order" integer NOT NULL,
    path character varying NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.photo OWNER TO sergei;

--
-- Name: photo_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.photo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.photo_id_seq OWNER TO sergei;

--
-- Name: photo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.photo_id_seq OWNED BY public.photo.id;


--
-- Name: purchase; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.purchase (
    id integer NOT NULL,
    start date NOT NULL,
    "end" date NOT NULL,
    price numeric(10,2) NOT NULL,
    prepayment numeric(10,2) NOT NULL,
    refund numeric(10,2) NOT NULL,
    is_paid boolean NOT NULL,
    is_prepayment_paid boolean NOT NULL,
    is_canceled boolean NOT NULL,
    order_id integer NOT NULL,
    room_id integer NOT NULL
);


ALTER TABLE public.purchase OWNER TO sergei;

--
-- Name: purchase_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.purchase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.purchase_id_seq OWNER TO sergei;

--
-- Name: purchase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.purchase_id_seq OWNED BY public.purchase.id;


--
-- Name: room; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.room (
    id integer NOT NULL,
    room_number integer NOT NULL,
    date_created timestamp without time zone NOT NULL,
    date_deleted timestamp without time zone,
    category_id integer NOT NULL
);


ALTER TABLE public.room OWNER TO sergei;

--
-- Name: room_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.room_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.room_id_seq OWNER TO sergei;

--
-- Name: room_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.room_id_seq OWNED BY public.room.id;


--
-- Name: sale; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.sale (
    id integer NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    discount double precision NOT NULL,
    image_path character varying NOT NULL,
    start_date timestamp without time zone NOT NULL,
    end_date timestamp without time zone NOT NULL,
    date_created timestamp without time zone NOT NULL,
    date_deleted timestamp without time zone
);


ALTER TABLE public.sale OWNER TO sergei;

--
-- Name: sale_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.sale_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.sale_id_seq OWNER TO sergei;

--
-- Name: sale_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.sale_id_seq OWNED BY public.sale.id;


--
-- Name: tag; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.tag (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.tag OWNER TO sergei;

--
-- Name: tag_id_seq; Type: SEQUENCE; Schema: public; Owner: sergei
--

CREATE SEQUENCE public.tag_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tag_id_seq OWNER TO sergei;

--
-- Name: tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: sergei
--

ALTER SEQUENCE public.tag_id_seq OWNED BY public.tag.id;


--
-- Name: user_group; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.user_group (
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.user_group OWNER TO sergei;

--
-- Name: worker; Type: TABLE; Schema: public; Owner: sergei
--

CREATE TABLE public.worker (
    id integer NOT NULL,
    salary numeric NOT NULL
);


ALTER TABLE public.worker OWNER TO sergei;

--
-- Name: base_order id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.base_order ALTER COLUMN id SET DEFAULT nextval('public.base_order_id_seq'::regclass);


--
-- Name: category id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.category ALTER COLUMN id SET DEFAULT nextval('public.category_id_seq'::regclass);


--
-- Name: group id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public."group" ALTER COLUMN id SET DEFAULT nextval('public.group_id_seq'::regclass);


--
-- Name: people id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.people ALTER COLUMN id SET DEFAULT nextval('public.people_id_seq'::regclass);


--
-- Name: permission id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.permission ALTER COLUMN id SET DEFAULT nextval('public.permission_id_seq'::regclass);


--
-- Name: photo id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.photo ALTER COLUMN id SET DEFAULT nextval('public.photo_id_seq'::regclass);


--
-- Name: purchase id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.purchase ALTER COLUMN id SET DEFAULT nextval('public.purchase_id_seq'::regclass);


--
-- Name: room id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.room ALTER COLUMN id SET DEFAULT nextval('public.room_id_seq'::regclass);


--
-- Name: sale id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.sale ALTER COLUMN id SET DEFAULT nextval('public.sale_id_seq'::regclass);


--
-- Name: tag id; Type: DEFAULT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.tag ALTER COLUMN id SET DEFAULT nextval('public.tag_id_seq'::regclass);


--
-- Data for Name: base_order; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.base_order (id, date_created, type) FROM stdin;
1	2023-03-27 14:12:14.501407	order
2	2023-03-29 17:26:55.047396	order
3	2023-03-29 17:29:22.846724	order
4	2023-03-29 17:31:46.460373	order
5	2023-03-29 17:32:35.138039	order
6	2023-03-30 17:52:19.547558	order
\.


--
-- Data for Name: cart; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.cart (id, cart_uuid) FROM stdin;
\.


--
-- Data for Name: category; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.category (id, name, description, price, prepayment_percent, refund_percent, main_photo_path, rooms_count, floors, beds, square, date_created, date_deleted, is_hidden) FROM stdin;
2	Двухэтажный домик	крутой жесть	5000	10	10	C:\\photos\\1.png	3	2	5	40.5	2023-03-27 14:10:38.35022	\N	f
3	Терхметный люкс	Дорого-богато	999.99	20	50	J:\\photos\\9.png	2	1	3	65.5	2023-03-28 19:39:12.931121	\N	f
4	sadsad	asdsadd	500.0	10	10	C:\\...	3	2	3	52	2023-03-30 14:42:02.821416	\N	f
5	sadsad	asdsadd	500.0	10	10	C:\\...	3	2	3	52	2023-03-30 15:30:22.838675	\N	f
\.


--
-- Data for Name: category_sale; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.category_sale (sale_id, category_id) FROM stdin;
\.


--
-- Data for Name: category_tag; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.category_tag (tag_id, category_id) FROM stdin;
1	3
1	4
4	2
\.


--
-- Data for Name: client; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.client (id, date_of_birth) FROM stdin;
1	2000-03-15
2	\N
3	\N
\.


--
-- Data for Name: client_order; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.client_order (id, comment, paid, refunded, date_full_prepayment, date_full_paid, date_finished, date_canceled, client_id) FROM stdin;
4	\N	0	0	\N	\N	\N	\N	1
5	\N	0	0	\N	\N	\N	\N	1
3	\N	46499.99	0	2023-03-30 12:32:41.670609	2023-03-30 12:42:00.464354	\N	2023-03-30 13:40:48.445535	1
2	\N	20000.00	0	\N	2023-03-30 13:47:17.177769	\N	2023-03-30 13:49:58.914054	1
6	\N	0	0	\N	\N	\N	\N	1
\.


--
-- Data for Name: group; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public."group" (id, name) FROM stdin;
1	Администратор ресепшена
\.


--
-- Data for Name: group_permission; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.group_permission (group_id, permission_id) FROM stdin;
1	1
\.


--
-- Data for Name: people; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.people (id, first_name, last_name, email, password, date_created, date_deleted, type) FROM stdin;
1	Bob	\N	asdasd@asd.ru	$2b$12$C5U6Y814h6u1iCYvflXTqOlZQLxVrh08opT97iwpr6Wj7FnYcRzHG	2023-03-29 16:22:02.505722	\N	client
3	\N	\N	sg2@mail.ru	$2b$12$DworKNxApt2pyuhk1OTviuiGLX5M32gXqWu14Yjnin/Qk/a48/IKm	2023-03-31 20:10:40.275455	\N	client
2	\N	\N	sg@mail.ru	$2b$12$yz/DEfEDBtPHkjujmGYVhunEVBgJrS4g1tyunCwVzzj4pSSvNnPba	2023-03-31 19:48:26.531404	\N	client
4	Alexey	Petrov	worker@mail.ru	\N	2023-04-01 14:15:00.905613	\N	worker
8	\N	\N	worker2@mail.ru	\N	2023-04-01 14:54:54.570626	\N	worker
9	\N	Dmitriy	worker3@mail.ru	qwe	2023-04-01 14:55:53.670414	\N	worker
10	\N	\N	admin@gmail.ru	$2b$12$yg4IacrqHNcMrCs8vsAy/.GyI6kdqjssBUm8pWddTuAhNJjF4Rs92	2023-04-01 14:58:49.408842	\N	worker
\.


--
-- Data for Name: permission; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.permission (id, name, code) FROM stdin;
1	просмотр клиентов	show_client
2	редактирование клиентов	edit_client
3	добавление клиентов	add_client
5	просмотр номеров	show_room
6	редактирование номеров	edit_room
7	удаление номеров	delete_room
8	просмотр категорий	show_category
9	редактирование категорий	edit_category
10	удаление категорий	delete_category
11	просмотр тегов	show_tag
12	редактирование тегов	edit_tag
13	удаление тегов	delete_tag
14	добавление тегов	add_tag
15	добавление номеров	add_room
16	добавление категорий	add_category
17	добавление скидок	add_sale
18	редактирование скидок	edit_sale
19	просмотр скидок	show_sale
20	удаление скидок	delete_sale
21	добавление фотографий	add_photo
22	редактирование фотографий	edit_photo
23	просмотр фотографий	show_photo
24	удаление фотографий	delete_photo
25	добавление групп	add_group
26	редактирование групп	edit_group
27	просмотр гупп	show_group
28	удаление групп	delete_group
29	добавление сотрудников	add_worker
30	редактирование сотрудников	edit_worker
31	просмотр сотрудников	show_worker
32	удаление сотрудников	delete_worker
33	удаление клиентов	delete_client
34	добавление заказов	add_order
35	редактирование заказов	edit_order
36	просмотр заказов	show_order
37	отмена заказов	cancel_order
38	добавление покупок	add_purchase
39	редактирование покупок	edit_purchase
40	отмена покупок	cancel_purchase
41	просмотр покупок	show_purchase
\.


--
-- Data for Name: photo; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.photo (id, "order", path, category_id) FROM stdin;
3	1	C:\\img\\2.png	2
4	4	C:\\asd\\qwe.jpg	2
6	2	C:\\asd\\qwe.jpg	2
8	6	C:\\asd\\qwe.jpg	2
5	3	C:\\asd\\qwe.jpg	2
7	5	C:\\asd\\qwe.jpg	2
\.


--
-- Data for Name: purchase; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.purchase (id, start, "end", price, prepayment, refund, is_paid, is_prepayment_paid, is_canceled, order_id, room_id) FROM stdin;
\.


--
-- Data for Name: room; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.room (id, room_number, date_created, date_deleted, category_id) FROM stdin;
1	1	2023-03-27 14:10:38.344425	\N	2
6	6	2023-03-28 14:07:57.638473	\N	2
7	7	2023-03-28 14:07:57.638473	\N	2
15	8	2023-03-28 14:45:37.591384	\N	2
16	9	2023-03-28 14:46:46.326785	\N	2
17	10	2023-03-28 14:46:46.326785	\N	2
18	11	2023-03-28 14:46:46.326785	\N	2
19	12	2023-03-28 14:46:46.326785	\N	2
20	13	2023-03-28 15:04:11.789762	\N	2
21	14	2023-03-28 16:23:31.776538	\N	2
22	15	2023-03-28 16:24:45.920833	\N	2
2	20	2023-03-28 14:04:22.425019	\N	2
23	55	2023-03-28 19:00:22.332037	\N	2
28	56	2023-03-28 19:09:12.472202	\N	2
29	57	2023-03-29 21:19:57.333875	\N	3
30	58	2023-03-30 17:52:19.554246	\N	3
3	3	2023-03-28 14:05:32.653915	2023-03-30 19:24:38.446194	2
4	4	2023-03-28 14:05:32.653915	2023-03-30 19:25:28.494328	2
5	44	2023-03-28 14:05:32.653915	\N	2
\.


--
-- Data for Name: sale; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.sale (id, name, description, discount, image_path, start_date, end_date, date_created, date_deleted) FROM stdin;
1	Апрельские скидки	Lorem ipsum...	20	D:\\images\\sales\\1.jpg	2023-03-29 10:00:00	2023-04-18 20:00:00	2023-03-30 17:22:25.441535	\N
\.


--
-- Data for Name: tag; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.tag (id, name) FROM stdin;
1	Красиво
4	qweasd
10	tag2
\.


--
-- Data for Name: user_group; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.user_group (user_id, group_id) FROM stdin;
4	1
10	1
\.


--
-- Data for Name: worker; Type: TABLE DATA; Schema: public; Owner: sergei
--

COPY public.worker (id, salary) FROM stdin;
4	4999.0
8	4999.0
9	4999.0
10	99999.0
\.


--
-- Name: base_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.base_order_id_seq', 6, true);


--
-- Name: category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.category_id_seq', 5, true);


--
-- Name: group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.group_id_seq', 1, true);


--
-- Name: people_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.people_id_seq', 10, true);


--
-- Name: permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.permission_id_seq', 41, true);


--
-- Name: photo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.photo_id_seq', 9, true);


--
-- Name: purchase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.purchase_id_seq', 1, true);


--
-- Name: room_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.room_id_seq', 30, true);


--
-- Name: sale_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.sale_id_seq', 1, true);


--
-- Name: tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: sergei
--

SELECT pg_catalog.setval('public.tag_id_seq', 10, true);


--
-- Name: base_order base_order_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.base_order
    ADD CONSTRAINT base_order_pkey PRIMARY KEY (id);


--
-- Name: cart cart_cart_uuid_key; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_cart_uuid_key UNIQUE (cart_uuid);


--
-- Name: cart cart_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_pkey PRIMARY KEY (id);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: category_sale category_sale_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.category_sale
    ADD CONSTRAINT category_sale_pkey PRIMARY KEY (sale_id, category_id);


--
-- Name: category_tag category_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.category_tag
    ADD CONSTRAINT category_tag_pkey PRIMARY KEY (tag_id, category_id);


--
-- Name: client_order client_order_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.client_order
    ADD CONSTRAINT client_order_pkey PRIMARY KEY (id);


--
-- Name: client client_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_pkey PRIMARY KEY (id);


--
-- Name: group group_name_key; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_name_key UNIQUE (name);


--
-- Name: group_permission group_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.group_permission
    ADD CONSTRAINT group_permission_pkey PRIMARY KEY (group_id, permission_id);


--
-- Name: group group_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public."group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- Name: people people_email_key; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.people
    ADD CONSTRAINT people_email_key UNIQUE (email);


--
-- Name: people people_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.people
    ADD CONSTRAINT people_pkey PRIMARY KEY (id);


--
-- Name: permission permission_code_key; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.permission
    ADD CONSTRAINT permission_code_key UNIQUE (code);


--
-- Name: permission permission_name_key; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.permission
    ADD CONSTRAINT permission_name_key UNIQUE (name);


--
-- Name: permission permission_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.permission
    ADD CONSTRAINT permission_pkey PRIMARY KEY (id);


--
-- Name: photo photo_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.photo
    ADD CONSTRAINT photo_pkey PRIMARY KEY (id);


--
-- Name: purchase purchase_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.purchase
    ADD CONSTRAINT purchase_pkey PRIMARY KEY (id);


--
-- Name: room room_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_pkey PRIMARY KEY (id);


--
-- Name: sale sale_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.sale
    ADD CONSTRAINT sale_pkey PRIMARY KEY (id);


--
-- Name: tag tag_name_key; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_name_key UNIQUE (name);


--
-- Name: tag tag_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.tag
    ADD CONSTRAINT tag_pkey PRIMARY KEY (id);


--
-- Name: user_group user_group_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.user_group
    ADD CONSTRAINT user_group_pkey PRIMARY KEY (user_id, group_id);


--
-- Name: worker worker_pkey; Type: CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.worker
    ADD CONSTRAINT worker_pkey PRIMARY KEY (id);


--
-- Name: cart cart_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.cart
    ADD CONSTRAINT cart_id_fkey FOREIGN KEY (id) REFERENCES public.base_order(id);


--
-- Name: category_sale category_sale_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.category_sale
    ADD CONSTRAINT category_sale_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id);


--
-- Name: category_sale category_sale_sale_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.category_sale
    ADD CONSTRAINT category_sale_sale_id_fkey FOREIGN KEY (sale_id) REFERENCES public.sale(id);


--
-- Name: category_tag category_tag_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.category_tag
    ADD CONSTRAINT category_tag_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id);


--
-- Name: category_tag category_tag_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.category_tag
    ADD CONSTRAINT category_tag_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tag(id);


--
-- Name: client client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.client
    ADD CONSTRAINT client_id_fkey FOREIGN KEY (id) REFERENCES public.people(id);


--
-- Name: client_order client_order_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.client_order
    ADD CONSTRAINT client_order_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.people(id);


--
-- Name: client_order client_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.client_order
    ADD CONSTRAINT client_order_id_fkey FOREIGN KEY (id) REFERENCES public.base_order(id);


--
-- Name: group_permission group_permission_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.group_permission
    ADD CONSTRAINT group_permission_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."group"(id);


--
-- Name: group_permission group_permission_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.group_permission
    ADD CONSTRAINT group_permission_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.permission(id);


--
-- Name: photo photo_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.photo
    ADD CONSTRAINT photo_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id);


--
-- Name: purchase purchase_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.purchase
    ADD CONSTRAINT purchase_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.base_order(id);


--
-- Name: purchase purchase_room_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.purchase
    ADD CONSTRAINT purchase_room_id_fkey FOREIGN KEY (room_id) REFERENCES public.room(id);


--
-- Name: room room_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.room
    ADD CONSTRAINT room_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.category(id);


--
-- Name: user_group user_group_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.user_group
    ADD CONSTRAINT user_group_group_id_fkey FOREIGN KEY (group_id) REFERENCES public."group"(id);


--
-- Name: user_group user_group_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.user_group
    ADD CONSTRAINT user_group_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.people(id);


--
-- Name: worker worker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: sergei
--

ALTER TABLE ONLY public.worker
    ADD CONSTRAINT worker_id_fkey FOREIGN KEY (id) REFERENCES public.people(id);


--
-- PostgreSQL database dump complete
--

