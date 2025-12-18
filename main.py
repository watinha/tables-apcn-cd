import pandas as pd


from lib import generate_orientacoes_table, read_orientadores_file


if __name__ == "__main__":
    orientadores = read_orientadores_file('./data/orientadores.txt')

    df = pd.read_excel('./data/orientacoes.xlsx', skiprows=[0, 1, 2])
    orientacoes_table = generate_orientacoes_table(df, orientadores)
    orientacoes_table.to_excel('./results/orientacoes_table.xlsx', index=False)


    
