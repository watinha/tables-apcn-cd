import pandas as pd


from lib import generate_orientacoes_table, read_orientadores_file, generate_bibliographic_prod_table, generate_prod_tec_table


if __name__ == "__main__":
    orientadores = read_orientadores_file('./data/orientadores.txt')

    df = pd.read_excel('./data/orientacoes.xlsx', skiprows=[0, 1, 2])
    orientacoes_table = generate_orientacoes_table(df, orientadores)
    orientacoes_table.to_excel('./results/orientacoes_table.xlsx', index=False)
    print("Orientações table generated successfully!")

    df = pd.read_excel('./data/producao-bibliografica.xlsx', skiprows=[0, 1, 2])
    prod_by_orientadores = generate_bibliographic_prod_table(df, orientadores)
    prod_by_orientadores.to_excel('./results/bibliographic_production_table.xlsx', index=False)
    print("Bibliographic Production table generated successfully!")

    df = pd.read_excel('./data/producao-tecnica.xlsx', skiprows=[0, 1, 2])
    prod_by_orientadores = generate_prod_tec_table(df, orientadores)
    prod_by_orientadores.to_excel('./results/producao-tecnica.xlsx', index=False)
    print("Bibliographic Production table generated successfully!")
    
