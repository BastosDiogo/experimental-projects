import sqlite3
from uuid import uuid1, uuid4, uuid5
from datetime import datetime, timezone


class BancoDados():
    """Classe responsável por armazenar todos os dados"""
    def __init__(self, tabela:str=''):
        self._tabela = tabela

    @property
    def tabela(self):
        return self._tabela

    @property
    def data_base(self):
        return "eleicao_db.db"

    @property
    def conectar_db(self):
        # Conecta (ou cria) o banco
        conn = sqlite3.connect(self.data_base)

        # Retorna o cursor
        return conn.cursor()


    def criar_banco_dados(self):
        """Cria o banco de dados"""
        try:
            print('Criando as tabelas...')
            # Cria cursor
            cursor = self.conectar_db

            # Cria tabela
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS candidatos (
                id CHAR(36) UNIQUE NOT NULL,
                nome VARCHAR(255) UNIQUE NOT NULL,
                cpf CHAR(11) UNIQUE NOT NULL,
                numero_candidato INTEGER UNIQUE NOT NULL
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS votos (
                id CHAR(36) UNIQUE NOT NULL,
                cpf CHAR(11) NOT NULL,
                numero_candidato INTEGER NOT NULL,
                data_votacao TIMESTAMP NOT NULL
            )
            """)

            cursor.close()
            print('Tabelas criadas com sucesso!')
            return True

        except Exception as erro:
            print(f'O seguinte erro foi encontrado:\n{erro}')
            return False


    def inserir_dados(self, payload:dict):
        """Insere os dados no database."""
        # Conecta (ou cria) o banco
        conn = sqlite3.connect(self.data_base)

        # Cria cursor
        cursor = conn.cursor()

        tupla_chaves = tuple(payload.keys())
        campos = ', '.join(tupla_chaves)
        interrogacoes = ('?, ' * len(tupla_chaves))[0:-2]

        try:
            print(f'Inserindo os dados na tabela: {self.tabela}\nDados:{payload}')
            # Insere dados
            cursor.execute(
                f"INSERT INTO {self.tabela} ({campos}) VALUES ({interrogacoes})",
                tuple(payload.values())
            )

            # Confirma alterações
            conn.commit()

            # Fecha conexão
            conn.close()
            return True

        except Exception as erro:
            print(f'O seguinte erro foi encontrado:\n{erro}')
            return False

    def comandos_gerais(self, comando_sql:str):
        """Executa comandos SQL em geral."""
        # Conecta (ou cria) o banco
        conn = sqlite3.connect(self.data_base)

        # Cria cursor
        cursor = conn.cursor()

        try:
            #print(f'Comando utilizado: {comando_sql}')
            # Executando comando
            cursor.execute(comando_sql)
            #cursor.execute("SELECT * FROM candidatos")

            #consulta = cursor.fetchall()
            #dados = consulta[0] if consulta else []
            dados = cursor.fetchall()
            #print(dados)

            # # Confirma alterações
            # conn.commit()

            # Fecha conexão
            conn.close()
            return (True, dados)

        except Exception as erro:
            print(f'O seguinte erro foi encontrado:\n{erro}')
            return (False, [])


class TratarDados():
    """Classe com os métodos para tratar os dados das tabelas."""

    def tratar_dados_gerais(self, payload:dict, payload_votos:bool=False):
        """Faz o tratamento dos dados de entrad nas tabelas"""
        payload = {
            'id': str(payload['id']),
            'nome': str(payload.get('nome', '')).title(),
            'cpf': str(payload['cpf']).replace('.','').replace('-', ''),
            'numero_candidato': int(payload['numero_candidato'])
        }

        if payload_votos:
            payload['data_votacao'] = datetime.now(tz=timezone.utc).isoformat()
            payload.pop('nome')

        return payload


    def formatar_tabela_candidatos(
        self,
        dados: list[tuple],
        campos_tabela: tuple[str, str] = ("Coluna 1", "Coluna 2"),
        contabilizar_votos: bool = False
    ) -> str:
        """
        dados: lista de tuplas [(valor_coluna1, valor_coluna2), ...]
        campos_tabela: nomes das duas colunas
        contabilizar_votos: se True, adiciona linha de total ao final
        """

        if not dados:
            return "\nNenhum registro encontrado.\n"

        nome_coluna1, nome_coluna2 = campos_tabela

        # Se precisar contabilizar
        total_geral = sum(valor2 for _, valor2 in dados) if contabilizar_votos else None

        # Descobrir larguras dinâmicas
        largura_col1 = max(
            max(len(str(valor1)) for valor1, _ in dados),
            len(nome_coluna1),
            len("Total de Votos") if contabilizar_votos else 0
        )

        largura_col2 = max(
            max(len(str(valor2)) for _, valor2 in dados),
            len(nome_coluna2),
            len(str(total_geral)) if contabilizar_votos else 0
        )

        # Montar tabela
        tabela = "\n"
        tabela += f"{nome_coluna1:<{largura_col1}} | {nome_coluna2:>{largura_col2}}\n"
        tabela += "-" * (largura_col1 + largura_col2 + 3) + "\n"

        for valor1, valor2 in dados:
            tabela += f"{str(valor1):<{largura_col1}} | {str(valor2):>{largura_col2}}\n"

        if contabilizar_votos:
            tabela += "-" * (largura_col1 + largura_col2 + 3) + "\n"
            tabela += f"{'Total de Votos':<{largura_col1}} | {total_geral:>{largura_col2}}\n"

        return tabela


    def escrever_arquivo(self, arquivos:list):
        """Função para escrever o arquivo com os dados gerados."""
        caminho_arquivo = 'extratificacao_votos.txt'
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            for arq in arquivos:
                linha = {
                    'id': arq[0],
                    'cpf': arq[1],
                    'numero_candidato': arq[2],
                    'data_votacao': arq[3]
                }
                arquivo.writelines(f'{linha}\n')

        return caminho_arquivo


class Cadidatos(BancoDados):
    """Classe para criar os candidatos"""
    def __init__(self, tabela = 'candidatos'):
        super().__init__(tabela)

    def add_candidados(self, payload:dict[str]):
        """Função para armazenar os dados de candidados."""
        payload['id'] = str(uuid1())
        return self.inserir_dados(TratarDados().tratar_dados_gerais(payload))

    def vizualizar_dados(self):
        """Método para vizualizar os dados no database."""
        print(f'\nConsultando a tabela de {self.tabela}...\n')
        consulta = self.comandos_gerais(
            f'SELECT nome, numero_candidato FROM {self.tabela} ORDER BY numero_candidato'
        )

        if not consulta[0]:
            return ''

        mostrar_dados_SEM_nulos = consulta[1][:-1]
        vizualizacao = TratarDados().formatar_tabela_candidatos(
            mostrar_dados_SEM_nulos,
            campos_tabela=("Nome Candidato", "Número do Candidato")
        )

        return vizualizacao


    def criar_nulo(self):
        """Registro para salvar os votos nulos."""
        payload = {
            'nome': 'Votos Nulos',
            'cpf': '-',
            'numero_candidato': 999
        }
        Cadidatos().add_candidados(payload)


class Votos(BancoDados):
    """Classe para adicionar os votos"""
    def __init__(self, tabela = 'votos'):
        super().__init__(tabela)


    def add_votos(self, numero_candidato:int):
        """Função para armazenar os dados de votos."""
        candidato = Cadidatos().comandos_gerais(
            f'SELECT cpf, numero_candidato FROM candidatos where numero_candidato = {numero_candidato}'
        )
        payload = {'id': str(uuid4())}

        if not candidato[1]:
            print(f'O candidato número {numero_candidato}, não existe na database. Voto NULO!')
            payload.update({'numero_candidato': 999, 'cpf': '-'})
            self.inserir_dados(TratarDados().tratar_dados_gerais(payload, payload_votos=True))
            return False

        for dados_candidato in candidato[1]:
            payload = {
                'id': str(uuid4()),
                'numero_candidato': dados_candidato[1],
                'cpf': dados_candidato[0]
            }

            self.inserir_dados(TratarDados().tratar_dados_gerais(payload, payload_votos=True))

        return True

    def contagem(self):
        """Método para retornar o total de votos."""
        votos = self.comandos_gerais(
        f"""SELECT
                MAX(candidatos.nome) AS nome_candidatos, COUNT({self.tabela}.cpf) AS votos
            FROM {self.tabela}
            JOIN candidatos ON candidatos.numero_candidato = {self.tabela}.numero_candidato
            GROUP BY {self.tabela}.cpf
            ORDER BY votos desc
        """
        )[1]

        vizualizacao = TratarDados().formatar_tabela_candidatos(
            votos,
            campos_tabela=("Nome Candidato", "Total Votos"),
            contabilizar_votos=True
        )
        print(f'{vizualizacao}')
        return votos

    def extratificacao_votos(self):
        """Cria um TXT com todos os votos do database."""
        votos = self.comandos_gerais(f'SELECT * FROM {self.tabela}')[1]
        return TratarDados().escrever_arquivo(votos)
