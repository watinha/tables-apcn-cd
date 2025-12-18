import pandas as pd


def read_orientadores_file(file_path):
    with open(file_path, 'r', encoding='latin1') as file:
        orientadores = [line.split(';')[0] for line in file]

    return orientadores


def generate_orientacoes_table (df, orientadores):
    informadaPor = df['Informada por'].unique()
    orientadores_query = []
    for orientador in orientadores:
        orientador_list = [orientador]
        for informada in informadaPor:
            if orientador in informada:
                orientador_list.append(informada)
        orientadores_query.append(orientador_list)

    tipo_de_orientacoes = df['Tipo da produção'].unique()
    orientacoes_data = []

    for orientador in orientadores_query:
        query = None
        orientacoes_rows = []

        if isinstance(orientador, list):
            query = df['Informada por'] == orientador[0]
            for i in range(1, len(orientador)):
                query |= df['Informada por'] == orientador[i]
            orientador_df = df[query]
            orientacoes_rows.append(orientador[0])
        else:
            orientador_df = df[df['Informada por'] == orientador]
            orientacoes_rows.append(orientador)

        for tipo in tipo_de_orientacoes:
            count = orientador_df[orientador_df['Tipo da produção'] == tipo].shape[0]
            orientacoes_rows.append(count)

        orientacoes_data.append(orientacoes_rows)

    return pd.DataFrame(orientacoes_data, columns=['Orientador'] + list(tipo_de_orientacoes))


