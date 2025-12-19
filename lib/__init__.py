import pandas as pd, chevron, math


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

        outros = orientador_df[orientador_df['Tipo da produção'] != 'Artigo publicado em periódicos']
        outros_sorted = ['Trabalho publicado em anais de evento', 'Organização de obra publicada', 'Capítulo de livro publicado', 'Livro publicado']
        outros_count = outros['Tipo da produção'].value_counts()
        for outro_tipo in outros_sorted:
            if (outro_tipo in outros_count.keys().tolist()):
                orientador_row.append(int(outros_count[outro_tipo]))
            else:
                orientador_row.append(0)

        bibliographic_prod_data.append(orientador_row)

    return pd.DataFrame(bibliographic_prod_data, columns=['Orientador', 'A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'B4', 'C', 'NP', 'Trabalhos publicados em anais de eventos', 'Organização de obra publicada', 'Capítulo de livro publicado', 'Livro publicado'])
    

def generate_prod_tec_table (df, orientadores):
    prod_by_orientador = _get_prod_by_orientador(df, orientadores)
    tipo_de_producao = df['Tipo da produção'].unique()
    prod_tec_data = []

    for orientador in orientadores:
        orientador_row = [orientador]
        orientador_df = prod_by_orientador[orientador]

        tipos_tec = [
            'Apresentação de Trabalho e palestra',
            'Trabalhos técnicos',
            'Programa de computador'
        ]

        prod_tec_counts = orientador_df['Tipo da produção'].value_counts()
        for tipo_tec in tipos_tec:
            if (tipo_tec in prod_tec_counts.keys().tolist()):
                orientador_row.append(int(prod_tec_counts[tipo_tec]))
            else:
                orientador_row.append(0)

        prod_tec_data.append(orientador_row)


    return pd.DataFrame(prod_tec_data, columns=['Orientador'] + tipos_tec)


def generate_producao_nominal (df_bib, df_tec, orientadores):
    full_report = []

    bib_prod_por_orientador = _get_prod_by_orientador(df_bib, orientadores)
    tec_prod_por_orientador = _get_prod_by_orientador(df_tec, orientadores)

    for orientador in orientadores:
        orientador_report = f'{orientador}\n - Produção Bibliográfica:\n------------------------------------\n'
        producoes = []
        
        bib_df = bib_prod_por_orientador[orientador]
        tec_df = tec_prod_por_orientador[orientador]
    
        for index, row in bib_df.iterrows():
            with open('templates/artigo.txt', 'r', encoding='utf-8') as f:
                if str(row['ISSN Periódico']) == 'nan':
                    issn = 'N/A'
                    snip = 'N/A'
                    sjr = 'N/A'
                else:
                    issn = row['ISSN Periódico']
                    snip = row['Source Normalized Impact per Paper (SNIP) – Scopus atual (2024)']
                    sjr = row['SCImago Journal Rank (SJR) – Scopus atual (2024)']

                params = {
                    'titulo': row['Título da produção'],
                    'tipo_producao': row['Tipo da produção'],
                    'issn': issn,
                    'periodico_evento': row['Periódico/Evento'],
                    'ano': row['Ano da produção'],
                    'qualis': row['Estrato Qualis (2017/2020) oficial'],
                    'snip': snip,
                    'sjr': sjr,
                    'referencia': row['ABNT']
                }

                number_of_authors = int(row['Total de autores'])
                authors = [] 
                for i in range(1, number_of_authors + 1):
                    author_key = f'Autor {i}'
                    authors.append(row[author_key])
                params['autores'] = ', '.join(authors)
                producoes.append(chevron.render(f, params))

        orientador_report += '\n------------------------------------\n'.join(producoes)

        full_report.append(orientador_report)

    with open('./results/producao-nominal.txt', 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(full_report))




