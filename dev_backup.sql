--
-- PostgreSQL database dump
--

\restrict 7sv7UK8YY5yopS22HFbHXIb0LA8XzmSefvtPXunc5oxw5zhZt7VNXMQupxgkvCb

-- Dumped from database version 18.3 (Postgres.app)
-- Dumped by pg_dump version 18.3 (Postgres.app)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO jonathandangeni;

--
-- Name: animal; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.animal (
    id integer NOT NULL,
    tag_number character varying(50),
    animal_type_id integer NOT NULL,
    purpose character varying(20),
    quantity integer,
    sex character varying(10),
    date_of_birth date,
    status character varying(20),
    notes text
);


ALTER TABLE public.animal OWNER TO jonathandangeni;

--
-- Name: animal_exit; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.animal_exit (
    id integer NOT NULL,
    animal_id integer NOT NULL,
    exit_type character varying(20),
    quantity integer,
    date date,
    notes text
);


ALTER TABLE public.animal_exit OWNER TO jonathandangeni;

--
-- Name: animal_exit_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.animal_exit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animal_exit_id_seq OWNER TO jonathandangeni;

--
-- Name: animal_exit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.animal_exit_id_seq OWNED BY public.animal_exit.id;


--
-- Name: animal_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.animal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animal_id_seq OWNER TO jonathandangeni;

--
-- Name: animal_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.animal_id_seq OWNED BY public.animal.id;


--
-- Name: animal_type; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.animal_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    breed character varying(100)
);


ALTER TABLE public.animal_type OWNER TO jonathandangeni;

--
-- Name: animal_type_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.animal_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.animal_type_id_seq OWNER TO jonathandangeni;

--
-- Name: animal_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.animal_type_id_seq OWNED BY public.animal_type.id;


--
-- Name: application; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.application (
    id integer NOT NULL,
    planting_id integer NOT NULL,
    inventory_item_id integer,
    date date,
    input_name character varying(200),
    quantity double precision,
    unit character varying(50),
    notes text
);


ALTER TABLE public.application OWNER TO jonathandangeni;

--
-- Name: application_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.application_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.application_id_seq OWNER TO jonathandangeni;

--
-- Name: application_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.application_id_seq OWNED BY public.application.id;


--
-- Name: birth; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.birth (
    id integer NOT NULL,
    breeding_event_id integer NOT NULL,
    birth_date date,
    offspring_breed character varying(100),
    male_offspring integer,
    female_offspring integer,
    notes text
);


ALTER TABLE public.birth OWNER TO jonathandangeni;

--
-- Name: birth_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.birth_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.birth_id_seq OWNER TO jonathandangeni;

--
-- Name: birth_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.birth_id_seq OWNED BY public.birth.id;


--
-- Name: breeding_event; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.breeding_event (
    id integer NOT NULL,
    male_id integer,
    female_id integer NOT NULL,
    male_breed character varying(100),
    female_breed character varying(100),
    breeding_type character varying(20),
    breeding_date date,
    expected_birth date,
    status character varying(20),
    notes text
);


ALTER TABLE public.breeding_event OWNER TO jonathandangeni;

--
-- Name: breeding_event_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.breeding_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.breeding_event_id_seq OWNER TO jonathandangeni;

--
-- Name: breeding_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.breeding_event_id_seq OWNED BY public.breeding_event.id;


--
-- Name: crop_type; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.crop_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    variety character varying(100),
    notes text
);


ALTER TABLE public.crop_type OWNER TO jonathandangeni;

--
-- Name: crop_type_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.crop_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.crop_type_id_seq OWNER TO jonathandangeni;

--
-- Name: crop_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.crop_type_id_seq OWNED BY public.crop_type.id;


--
-- Name: feed_record; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.feed_record (
    id integer NOT NULL,
    animal_id integer NOT NULL,
    feed_type_id integer,
    quantity double precision,
    unit character varying(20),
    date date,
    notes text
);


ALTER TABLE public.feed_record OWNER TO jonathandangeni;

--
-- Name: feed_record_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.feed_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feed_record_id_seq OWNER TO jonathandangeni;

--
-- Name: feed_record_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.feed_record_id_seq OWNED BY public.feed_record.id;


--
-- Name: feed_type; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.feed_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    default_unit character varying(20),
    notes text
);


ALTER TABLE public.feed_type OWNER TO jonathandangeni;

--
-- Name: feed_type_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.feed_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.feed_type_id_seq OWNER TO jonathandangeni;

--
-- Name: feed_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.feed_type_id_seq OWNED BY public.feed_type.id;


--
-- Name: field; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.field (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    size double precision,
    location character varying(200)
);


ALTER TABLE public.field OWNER TO jonathandangeni;

--
-- Name: field_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.field_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.field_id_seq OWNER TO jonathandangeni;

--
-- Name: field_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.field_id_seq OWNED BY public.field.id;


--
-- Name: finance_category; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.finance_category (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    type character varying(20),
    description character varying(200)
);


ALTER TABLE public.finance_category OWNER TO jonathandangeni;

--
-- Name: finance_category_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.finance_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.finance_category_id_seq OWNER TO jonathandangeni;

--
-- Name: finance_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.finance_category_id_seq OWNED BY public.finance_category.id;


--
-- Name: finance_transaction; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.finance_transaction (
    id integer NOT NULL,
    type character varying(20),
    category_id integer,
    description character varying(200),
    amount double precision,
    date date,
    notes text
);


ALTER TABLE public.finance_transaction OWNER TO jonathandangeni;

--
-- Name: finance_transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.finance_transaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.finance_transaction_id_seq OWNER TO jonathandangeni;

--
-- Name: finance_transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.finance_transaction_id_seq OWNED BY public.finance_transaction.id;


--
-- Name: harvest; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.harvest (
    id integer NOT NULL,
    planting_id integer NOT NULL,
    date date,
    quantity double precision,
    unit character varying(50),
    notes text
);


ALTER TABLE public.harvest OWNER TO jonathandangeni;

--
-- Name: harvest_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.harvest_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.harvest_id_seq OWNER TO jonathandangeni;

--
-- Name: harvest_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.harvest_id_seq OWNED BY public.harvest.id;


--
-- Name: health_record; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.health_record (
    id integer NOT NULL,
    animal_id integer NOT NULL,
    condition character varying(150),
    treatment character varying(150),
    medication character varying(150),
    date date,
    notes text
);


ALTER TABLE public.health_record OWNER TO jonathandangeni;

--
-- Name: health_record_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.health_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.health_record_id_seq OWNER TO jonathandangeni;

--
-- Name: health_record_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.health_record_id_seq OWNED BY public.health_record.id;


--
-- Name: inventory_category; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.inventory_category (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.inventory_category OWNER TO jonathandangeni;

--
-- Name: inventory_category_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.inventory_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inventory_category_id_seq OWNER TO jonathandangeni;

--
-- Name: inventory_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.inventory_category_id_seq OWNED BY public.inventory_category.id;


--
-- Name: inventory_item; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.inventory_item (
    id integer NOT NULL,
    name character varying(200) NOT NULL,
    category_id integer,
    quantity double precision,
    unit character varying(50)
);


ALTER TABLE public.inventory_item OWNER TO jonathandangeni;

--
-- Name: inventory_item_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.inventory_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.inventory_item_id_seq OWNER TO jonathandangeni;

--
-- Name: inventory_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.inventory_item_id_seq OWNED BY public.inventory_item.id;


--
-- Name: planting; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.planting (
    id integer NOT NULL,
    crop_type_id integer NOT NULL,
    field_id integer NOT NULL,
    planting_date date,
    expected_harvest date,
    status character varying(20)
);


ALTER TABLE public.planting OWNER TO jonathandangeni;

--
-- Name: planting_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.planting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.planting_id_seq OWNER TO jonathandangeni;

--
-- Name: planting_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.planting_id_seq OWNED BY public.planting.id;


--
-- Name: production; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.production (
    id integer NOT NULL,
    animal_id integer NOT NULL,
    product character varying(50),
    quantity double precision,
    unit character varying(20),
    date date,
    notes text
);


ALTER TABLE public.production OWNER TO jonathandangeni;

--
-- Name: production_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.production_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.production_id_seq OWNER TO jonathandangeni;

--
-- Name: production_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.production_id_seq OWNED BY public.production.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying(100) NOT NULL,
    password_hash character varying(200) NOT NULL,
    role character varying(50)
);


ALTER TABLE public.users OWNER TO jonathandangeni;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO jonathandangeni;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: weight_record; Type: TABLE; Schema: public; Owner: jonathandangeni
--

CREATE TABLE public.weight_record (
    id integer NOT NULL,
    animal_id integer NOT NULL,
    weight double precision,
    unit character varying(20),
    date date,
    notes text
);


ALTER TABLE public.weight_record OWNER TO jonathandangeni;

--
-- Name: weight_record_id_seq; Type: SEQUENCE; Schema: public; Owner: jonathandangeni
--

CREATE SEQUENCE public.weight_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.weight_record_id_seq OWNER TO jonathandangeni;

--
-- Name: weight_record_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jonathandangeni
--

ALTER SEQUENCE public.weight_record_id_seq OWNED BY public.weight_record.id;


--
-- Name: animal id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.animal ALTER COLUMN id SET DEFAULT nextval('public.animal_id_seq'::regclass);


--
-- Name: animal_exit id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.animal_exit ALTER COLUMN id SET DEFAULT nextval('public.animal_exit_id_seq'::regclass);


--
-- Name: animal_type id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.animal_type ALTER COLUMN id SET DEFAULT nextval('public.animal_type_id_seq'::regclass);


--
-- Name: application id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.application ALTER COLUMN id SET DEFAULT nextval('public.application_id_seq'::regclass);


--
-- Name: birth id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.birth ALTER COLUMN id SET DEFAULT nextval('public.birth_id_seq'::regclass);


--
-- Name: breeding_event id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.breeding_event ALTER COLUMN id SET DEFAULT nextval('public.breeding_event_id_seq'::regclass);


--
-- Name: crop_type id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.crop_type ALTER COLUMN id SET DEFAULT nextval('public.crop_type_id_seq'::regclass);


--
-- Name: feed_record id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.feed_record ALTER COLUMN id SET DEFAULT nextval('public.feed_record_id_seq'::regclass);


--
-- Name: feed_type id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.feed_type ALTER COLUMN id SET DEFAULT nextval('public.feed_type_id_seq'::regclass);


--
-- Name: field id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.field ALTER COLUMN id SET DEFAULT nextval('public.field_id_seq'::regclass);


--
-- Name: finance_category id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.finance_category ALTER COLUMN id SET DEFAULT nextval('public.finance_category_id_seq'::regclass);


--
-- Name: finance_transaction id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.finance_transaction ALTER COLUMN id SET DEFAULT nextval('public.finance_transaction_id_seq'::regclass);


--
-- Name: harvest id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.harvest ALTER COLUMN id SET DEFAULT nextval('public.harvest_id_seq'::regclass);


--
-- Name: health_record id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.health_record ALTER COLUMN id SET DEFAULT nextval('public.health_record_id_seq'::regclass);


--
-- Name: inventory_category id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.inventory_category ALTER COLUMN id SET DEFAULT nextval('public.inventory_category_id_seq'::regclass);


--
-- Name: inventory_item id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.inventory_item ALTER COLUMN id SET DEFAULT nextval('public.inventory_item_id_seq'::regclass);


--
-- Name: planting id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.planting ALTER COLUMN id SET DEFAULT nextval('public.planting_id_seq'::regclass);


--
-- Name: production id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.production ALTER COLUMN id SET DEFAULT nextval('public.production_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: weight_record id; Type: DEFAULT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.weight_record ALTER COLUMN id SET DEFAULT nextval('public.weight_record_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.alembic_version (version_num) FROM stdin;
0ba6a09a91e8
\.


--
-- Data for Name: animal; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.animal (id, tag_number, animal_type_id, purpose, quantity, sex, date_of_birth, status, notes) FROM stdin;
1	P1	1	breeding	1	Female	2025-06-04	active	
2	P2	1	breeding	1	Female	2025-06-04	active	
3	P3	1	breeding	1	Female	2025-06-04	active	
4	P4	1	breeding	1	Female	2025-06-04	active	
\.


--
-- Data for Name: animal_exit; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.animal_exit (id, animal_id, exit_type, quantity, date, notes) FROM stdin;
\.


--
-- Data for Name: animal_type; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.animal_type (id, name, breed) FROM stdin;
1	Pig	Cross Large White
\.


--
-- Data for Name: application; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.application (id, planting_id, inventory_item_id, date, input_name, quantity, unit, notes) FROM stdin;
\.


--
-- Data for Name: birth; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.birth (id, breeding_event_id, birth_date, offspring_breed, male_offspring, female_offspring, notes) FROM stdin;
\.


--
-- Data for Name: breeding_event; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.breeding_event (id, male_id, female_id, male_breed, female_breed, breeding_type, breeding_date, expected_birth, status, notes) FROM stdin;
1	\N	1	\N	\N	AI	2026-03-31	2026-07-18	pregnant	
4	\N	4	\N	\N	AI	2026-03-31	2026-07-18	pregnant	
3	\N	3	\N	\N	AI	2026-03-31	2026-07-18	pregnant	
2	\N	2	\N	\N	AI	2026-03-31	2026-07-18	pregnant	
\.


--
-- Data for Name: crop_type; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.crop_type (id, name, variety, notes) FROM stdin;
1	Maize	SC727	Hybrid Long Season, Draught resistant.
2	Tomato	Tengeru Select	Hybrid F2, determinant
3	Tomato	9081	Hybrid F1, indeterminate
4	Tomato	Chibli	Hybrid F2, determinate 
\.


--
-- Data for Name: feed_record; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.feed_record (id, animal_id, feed_type_id, quantity, unit, date, notes) FROM stdin;
\.


--
-- Data for Name: feed_type; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.feed_type (id, name, default_unit, notes) FROM stdin;
\.


--
-- Data for Name: field; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.field (id, name, size, location) FROM stdin;
\.


--
-- Data for Name: finance_category; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.finance_category (id, name, type, description) FROM stdin;
\.


--
-- Data for Name: finance_transaction; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.finance_transaction (id, type, category_id, description, amount, date, notes) FROM stdin;
\.


--
-- Data for Name: harvest; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.harvest (id, planting_id, date, quantity, unit, notes) FROM stdin;
\.


--
-- Data for Name: health_record; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.health_record (id, animal_id, condition, treatment, medication, date, notes) FROM stdin;
\.


--
-- Data for Name: inventory_category; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.inventory_category (id, name) FROM stdin;
\.


--
-- Data for Name: inventory_item; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.inventory_item (id, name, category_id, quantity, unit) FROM stdin;
\.


--
-- Data for Name: planting; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.planting (id, crop_type_id, field_id, planting_date, expected_harvest, status) FROM stdin;
\.


--
-- Data for Name: production; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.production (id, animal_id, product, quantity, unit, date, notes) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.users (id, username, password_hash, role) FROM stdin;
7	admin2	scrypt:32768:8:1$jXGVxhrwfMTgEphA$5fb3a5013a46a3c5621536d290e8a654883a06e8b5719cc5ce9be4d935c1cfb593e6e593c18108b3bb8836136c3d29c8e98935bdb8d6826931934b6617fe6393	admin
\.


--
-- Data for Name: weight_record; Type: TABLE DATA; Schema: public; Owner: jonathandangeni
--

COPY public.weight_record (id, animal_id, weight, unit, date, notes) FROM stdin;
\.


--
-- Name: animal_exit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.animal_exit_id_seq', 1, false);


--
-- Name: animal_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.animal_id_seq', 4, true);


--
-- Name: animal_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.animal_type_id_seq', 1, true);


--
-- Name: application_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.application_id_seq', 1, false);


--
-- Name: birth_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.birth_id_seq', 1, false);


--
-- Name: breeding_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.breeding_event_id_seq', 4, true);


--
-- Name: crop_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.crop_type_id_seq', 4, true);


--
-- Name: feed_record_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.feed_record_id_seq', 1, false);


--
-- Name: feed_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.feed_type_id_seq', 1, false);


--
-- Name: field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.field_id_seq', 1, false);


--
-- Name: finance_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.finance_category_id_seq', 1, false);


--
-- Name: finance_transaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.finance_transaction_id_seq', 1, false);


--
-- Name: harvest_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.harvest_id_seq', 1, false);


--
-- Name: health_record_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.health_record_id_seq', 1, false);


--
-- Name: inventory_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.inventory_category_id_seq', 1, false);


--
-- Name: inventory_item_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.inventory_item_id_seq', 1, false);


--
-- Name: planting_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.planting_id_seq', 1, false);


--
-- Name: production_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.production_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.users_id_seq', 7, true);


--
-- Name: weight_record_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jonathandangeni
--

SELECT pg_catalog.setval('public.weight_record_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: animal_exit animal_exit_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.animal_exit
    ADD CONSTRAINT animal_exit_pkey PRIMARY KEY (id);


--
-- Name: animal animal_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.animal
    ADD CONSTRAINT animal_pkey PRIMARY KEY (id);


--
-- Name: animal_type animal_type_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.animal_type
    ADD CONSTRAINT animal_type_pkey PRIMARY KEY (id);


--
-- Name: application application_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.application
    ADD CONSTRAINT application_pkey PRIMARY KEY (id);


--
-- Name: birth birth_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.birth
    ADD CONSTRAINT birth_pkey PRIMARY KEY (id);


--
-- Name: breeding_event breeding_event_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.breeding_event
    ADD CONSTRAINT breeding_event_pkey PRIMARY KEY (id);


--
-- Name: crop_type crop_type_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.crop_type
    ADD CONSTRAINT crop_type_pkey PRIMARY KEY (id);


--
-- Name: feed_record feed_record_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.feed_record
    ADD CONSTRAINT feed_record_pkey PRIMARY KEY (id);


--
-- Name: feed_type feed_type_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.feed_type
    ADD CONSTRAINT feed_type_pkey PRIMARY KEY (id);


--
-- Name: field field_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.field
    ADD CONSTRAINT field_pkey PRIMARY KEY (id);


--
-- Name: finance_category finance_category_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.finance_category
    ADD CONSTRAINT finance_category_pkey PRIMARY KEY (id);


--
-- Name: finance_transaction finance_transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.finance_transaction
    ADD CONSTRAINT finance_transaction_pkey PRIMARY KEY (id);


--
-- Name: harvest harvest_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.harvest
    ADD CONSTRAINT harvest_pkey PRIMARY KEY (id);


--
-- Name: health_record health_record_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.health_record
    ADD CONSTRAINT health_record_pkey PRIMARY KEY (id);


--
-- Name: inventory_category inventory_category_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.inventory_category
    ADD CONSTRAINT inventory_category_pkey PRIMARY KEY (id);


--
-- Name: inventory_item inventory_item_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.inventory_item
    ADD CONSTRAINT inventory_item_pkey PRIMARY KEY (id);


--
-- Name: planting planting_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.planting
    ADD CONSTRAINT planting_pkey PRIMARY KEY (id);


--
-- Name: production production_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.production
    ADD CONSTRAINT production_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: weight_record weight_record_pkey; Type: CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.weight_record
    ADD CONSTRAINT weight_record_pkey PRIMARY KEY (id);


--
-- Name: animal animal_animal_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.animal
    ADD CONSTRAINT animal_animal_type_id_fkey FOREIGN KEY (animal_type_id) REFERENCES public.animal_type(id);


--
-- Name: animal_exit animal_exit_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.animal_exit
    ADD CONSTRAINT animal_exit_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animal(id);


--
-- Name: application application_inventory_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.application
    ADD CONSTRAINT application_inventory_item_id_fkey FOREIGN KEY (inventory_item_id) REFERENCES public.inventory_item(id);


--
-- Name: application application_planting_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.application
    ADD CONSTRAINT application_planting_id_fkey FOREIGN KEY (planting_id) REFERENCES public.planting(id);


--
-- Name: birth birth_breeding_event_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.birth
    ADD CONSTRAINT birth_breeding_event_id_fkey FOREIGN KEY (breeding_event_id) REFERENCES public.breeding_event(id);


--
-- Name: breeding_event breeding_event_female_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.breeding_event
    ADD CONSTRAINT breeding_event_female_id_fkey FOREIGN KEY (female_id) REFERENCES public.animal(id);


--
-- Name: breeding_event breeding_event_male_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.breeding_event
    ADD CONSTRAINT breeding_event_male_id_fkey FOREIGN KEY (male_id) REFERENCES public.animal(id);


--
-- Name: feed_record feed_record_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.feed_record
    ADD CONSTRAINT feed_record_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animal(id);


--
-- Name: feed_record feed_record_feed_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.feed_record
    ADD CONSTRAINT feed_record_feed_type_id_fkey FOREIGN KEY (feed_type_id) REFERENCES public.feed_type(id);


--
-- Name: finance_transaction finance_transaction_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.finance_transaction
    ADD CONSTRAINT finance_transaction_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.finance_category(id);


--
-- Name: harvest harvest_planting_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.harvest
    ADD CONSTRAINT harvest_planting_id_fkey FOREIGN KEY (planting_id) REFERENCES public.planting(id);


--
-- Name: health_record health_record_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.health_record
    ADD CONSTRAINT health_record_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animal(id);


--
-- Name: inventory_item inventory_item_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.inventory_item
    ADD CONSTRAINT inventory_item_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.inventory_category(id);


--
-- Name: planting planting_crop_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.planting
    ADD CONSTRAINT planting_crop_type_id_fkey FOREIGN KEY (crop_type_id) REFERENCES public.crop_type(id);


--
-- Name: planting planting_field_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.planting
    ADD CONSTRAINT planting_field_id_fkey FOREIGN KEY (field_id) REFERENCES public.field(id);


--
-- Name: production production_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.production
    ADD CONSTRAINT production_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animal(id);


--
-- Name: weight_record weight_record_animal_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jonathandangeni
--

ALTER TABLE ONLY public.weight_record
    ADD CONSTRAINT weight_record_animal_id_fkey FOREIGN KEY (animal_id) REFERENCES public.animal(id);


--
-- PostgreSQL database dump complete
--

\unrestrict 7sv7UK8YY5yopS22HFbHXIb0LA8XzmSefvtPXunc5oxw5zhZt7VNXMQupxgkvCb

