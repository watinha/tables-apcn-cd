import pandas as pd


def read_orientadores_file(file_path):
    with open(file_path, 'r', encoding='latin1') as file:
        orientadores = [line.split(';')[0] for line in file]

    return orientadores


def _generate_orientadores_query (df, orientadores):
    informadaPor = df['Informada por'].unique()
    orientadores_query = []
    for orientador in orientadores:
        orientador_list = [orientador]
        for informada in informadaPor:
            if orientador in informada:
                orientador_list.append(informada)
        orientadores_query.append(orientador_list)

    return orientadores_query


def _get_prod_by_orientador (df, orientadores):
    prod_by_orientador = {}

    orientadores_query = _generate_orientadores_query(df, orientadores)

    for orientador in orientadores_query:
        query = None
        orientacoes_rows = []

        query = df['Informada por'] == orientador[0]
        for i in range(1, len(orientador)):
            query |= df['Informada por'] == orientador[i]
        orientador_df = df[query]

        prod_by_orientador[orientador[0]] = orientador_df

    return prod_by_orientador


def generate_orientacoes_table (df, orientadores):
    prod_by_orientador = _get_prod_by_orientador(df, orientadores)
    tipo_de_orientacoes = df['Tipo da produção'].unique()
    orientacoes_data = []

    for orientador in orientadores:
        orientacoes_rows = [orientador]
        orientador_df = prod_by_orientador[orientador]

        for tipo in tipo_de_orientacoes:
            count = orientador_df[orientador_df['Tipo da produção'] == tipo].shape[0]
            orientacoes_rows.append(count)

        orientacoes_data.append(orientacoes_rows)

    return pd.DataFrame(orientacoes_data, columns=['Orientador'] + list(tipo_de_orientacoes))


def generate_bibliographic_prod_table (df, orientadores):
    prod_by_orientador = _get_prod_by_orientador(df, orientadores)
    tipo_de_producao = df['Tipo da produção'].unique()
    bibliographic_prod_data = []

    for orientador in orientadores:
        orientador_row = [orientador]
        orientador_df = prod_by_orientador[orientador]
        periodicos = orientador_df[orientador_df['Tipo da produção'] == 'Artigo publicado em periódicos']
        
        qualis_counts = periodicos['Estrato Qualis (2017/2020) oficial'].value_counts()
        qualis_sorted = ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C', 'NP']
        qualis_counts_keys = qualis_counts.keys().tolist()
        for qualis in qualis_sorted:
            if (qualis in qualis_counts_keys):
                orientador_row.append(int(qualis_counts[qualis]))
            else:
                orientador_row.append(0)

        bibliographic_prod_data.append(orientador_row)

    return pd.DataFrame(bibliographic_prod_data, columns=['Orientador', 'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C', 'NP'])
    






