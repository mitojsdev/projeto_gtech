--Criação da TABELA DE CLIENTES
CREATE TABLE IF NOT EXISTS public."TB_CLIENTE"
(
    "ID_CLIENTE" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "NOME" text COLLATE pg_catalog."default" NOT NULL,
    "TELEFONE" text COLLATE pg_catalog."default" NOT NULL,
    "DATA_CADASTRO" date NOT NULL,
    CONSTRAINT "TB_CLIENTE_pkey1" PRIMARY KEY ("ID_CLIENTE")
)

TABLESPACE pg_default;

-- nome e telefone forma a chave única da tabela
CREATE UNIQUE INDEX IF NOT EXISTS idx_nome_telefone_unique
    ON public."TB_CLIENTE" USING btree
    ("NOME" COLLATE pg_catalog."default" ASC NULLS LAST, "TELEFONE" COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;


-- criação da tabela fornecedor
CREATE TABLE IF NOT EXISTS public."TB_FORNECEDOR"
(
    "ID_FORNECEDOR" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "NOME_EMPRESA" text COLLATE pg_catalog."default" NOT NULL,
    "TIPO_EMPRESA" text COLLATE pg_catalog."default" DEFAULT 'FISICA'::text,
    "DATA_CADASTRO" date NOT NULL,
    CONSTRAINT "TB_FORNECEDOR_pkey1" PRIMARY KEY ("ID_FORNECEDOR")
)

TABLESPACE pg_default;

-- nome da empresa e o seu tipo formam a chave única
CREATE UNIQUE INDEX IF NOT EXISTS idx_nome_empresa_tipo_unique
    ON public."TB_FORNECEDOR" USING btree
    ("NOME_EMPRESA" COLLATE pg_catalog."default" ASC NULLS LAST, "TIPO_EMPRESA" COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;


-- criação da tabela produto
CREATE TABLE IF NOT EXISTS public."TB_PRODUTO"
(
    "ID_PRODUTO" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "NOME" text COLLATE pg_catalog."default" NOT NULL,
    "PRECO_CUSTO" double precision NOT NULL,
    "TIPO_PRODUTO" integer NOT NULL,
    "FABRICANTE" text COLLATE pg_catalog."default",
    "MARCA" text COLLATE pg_catalog."default",
    "COR" text COLLATE pg_catalog."default",
    "ID_FORNECEDOR" integer NOT NULL,
    "DATA_CADASTRO" date NOT NULL,
    "ESTOQUE" integer NOT NULL,
    CONSTRAINT "TB_PRODUTO_pkey1" PRIMARY KEY ("ID_PRODUTO"),
    CONSTRAINT "TB_PRODUTO_ID_FORNECEDOR_fkey" FOREIGN KEY ("ID_FORNECEDOR")
        REFERENCES public."TB_FORNECEDOR" ("ID_FORNECEDOR") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "TB_PRODUTO_TIPO_PRODUTO_fkey" FOREIGN KEY ("TIPO_PRODUTO")
        REFERENCES public."TB_TIPO_PRODUTO" ("COD") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

-- chave única da tabela: nome do produto e fornecedor
CREATE UNIQUE INDEX IF NOT EXISTS idx_nome_id_fornecedor_unique
    ON public."TB_PRODUTO" USING btree
    ("NOME" COLLATE pg_catalog."default" ASC NULLS LAST, "ID_FORNECEDOR" ASC NULLS LAST)
    TABLESPACE pg_default;


-- criação da tabela TIPO_PRODUTO
CREATE TABLE IF NOT EXISTS public."TB_TIPO_PRODUTO"
(
    "COD" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "DESCRICAO" text COLLATE pg_catalog."default",
    "MARGEM" double precision,
    CONSTRAINT "TB_TIPO_PRODUTO_pkey1" PRIMARY KEY ("COD")
)

TABLESPACE pg_default;

-- criacão do índice usando 'descrição' como chave única
CREATE UNIQUE INDEX IF NOT EXISTS idx_tipo_produto_descricao_unique
    ON public."TB_TIPO_PRODUTO" USING btree
    ("DESCRICAO" COLLATE pg_catalog."default" ASC NULLS LAST)
    TABLESPACE pg_default;


-- criação da tabela de vendas
CREATE TABLE IF NOT EXISTS public."TB_VENDA"
(
    "ID" integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    "DATA" date NOT NULL,
    "ID_CLIENTE" integer,
    "ID_PRODUTO" integer,
    "QUANTIDADE" integer,
    "PRECO_VENDA" double precision NOT NULL,
    "LUCRO" double precision,
    CONSTRAINT "TB_VENDA_pkey1" PRIMARY KEY ("ID"),
    CONSTRAINT "TB_VENDA_ID_CLIENTE_fkey" FOREIGN KEY ("ID_CLIENTE")
        REFERENCES public."TB_CLIENTE" ("ID_CLIENTE") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT "TB_VENDA_ID_PRODUTO_fkey" FOREIGN KEY ("ID_PRODUTO")
        REFERENCES public."TB_PRODUTO" ("ID_PRODUTO") MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;


-- criação de trigger para diminuir o estoque na tabela de produtos a cada nova venda na tb_venda
CREATE OR REPLACE TRIGGER trigger_atualizar_estoque
    AFTER INSERT
    ON public."TB_VENDA"
    FOR EACH ROW
    EXECUTE FUNCTION public.atualizar_estoque();

-- função acionada pela trigger
CREATE OR REPLACE FUNCTION public.atualizar_estoque()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
BEGIN
    -- Verifica se a quantidade em estoque é suficiente
    IF (SELECT "ESTOQUE" FROM "TB_PRODUTO" WHERE "ID_PRODUTO" = NEW."ID_PRODUTO") < NEW."QUANTIDADE" THEN
        RAISE EXCEPTION 'Estoque insuficiente para o produto ID %', NEW."ID_PRODUTO";
    END IF;

    -- Atualiza a quantidade em estoque
    UPDATE "TB_PRODUTO"
    SET "ESTOQUE" = "ESTOQUE" - NEW."QUANTIDADE"
    WHERE "ID_PRODUTO" = NEW."ID_PRODUTO";

    RETURN NEW;
	
END;
$BODY$;

-- FIM SCRIPT --