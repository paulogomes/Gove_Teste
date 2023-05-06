import pandas as pd
import codecs
import re


# Ler a Base CSV
# foi necessario ler o arquivo com a lib codecs por causa do encoding do arquivo
def getLines(file):
    lines = codecs.open(file, 'r', encoding='ISO-8859-2')
    for i, line in enumerate(lines):
        if (i != 0):
            yield tuple(line.strip().split(';'))

df = pd.DataFrame(getLines('Arquivo_limpar.csv'), columns=['Cod Cliente', 'Nome', 'DocId (11 digitos)', 'endereco', 'seq', 'none'])

# Remove caracteres especias
df['endereco'] = df['endereco'].apply(lambda string: re.sub("[\.´`/:;-]","", string) )

#########################
# Tarefa 01
#########################

# Obtem campos por Regex
def apply_regex(string, group):
    r = re.compile('^\s?(rua|avenida|AV|R[,|\s]|TRAVESSA|TR)?(.*),\s?([0-9]{1,})?(.*)', re.IGNORECASE)
    match = r.match(string)
    if (match and match.group(group) != None):
        return match.group(group).strip()
    else:
        return ''

df['TIPO_LOGRADOURO'] = df['endereco'].apply(lambda string: apply_regex(string, 1))
df['NOME_LOGRADOURO'] = df['endereco'].apply(lambda string: apply_regex(string, 2))
df['NUMERO'] = df['endereco'].apply(lambda string: apply_regex(string, 3))
df['COMPLEMENTO'] = df['endereco'].apply(lambda string: apply_regex(string, 4))

# Limpa Campos
df['TIPO_LOGRADOURO'] = df['TIPO_LOGRADOURO'].apply(lambda string: string.upper())
df['TIPO_LOGRADOURO'] = df['TIPO_LOGRADOURO'].apply(lambda string: re.sub("^R$","RUA", string))
df['TIPO_LOGRADOURO'] = df['TIPO_LOGRADOURO'].apply(lambda string: re.sub("^AV$","AVENIDA", string))
df['TIPO_LOGRADOURO'] = df['TIPO_LOGRADOURO'].apply(lambda string: re.sub("^TR$","TRAVESSA", string))


# Exporta o resultado
df = df.drop('none', axis=1)
df.to_excel('tarefa_01.xlsx', index=False)

#########################
# Tarefa 03
#########################
df_DocId = df.loc[df['DocId (11 digitos)'] == '00000000000']
df_base = df.drop(df[df['DocId (11 digitos)'] == '00000000000'].index)

# Faz o join por endereço
df_endereco = pd.merge(df_DocId, df_base[['NOME_LOGRADOURO', 'NUMERO', 'Cod Cliente', 'Nome', 'DocId (11 digitos)']], how='inner', on=['NOME_LOGRADOURO', 'NUMERO'], suffixes=('', '_sugerido'))

# Faz o join por Cod Cliente
df_cod = pd.merge( df_DocId, df_base[['Cod Cliente', 'Nome', 'DocId (11 digitos)']], how='inner', on=['Cod Cliente'], suffixes=('', '_sugerido') )
df_cod = df_cod.drop_duplicates()

# Ajusta campos sugeridos
df_sugerido = pd.concat([df_endereco, df_cod], ignore_index=True)
df_sugerido['Cod Cliente'] = df_sugerido['Cod Cliente'].apply(lambda string: re.sub("^0$","", string))
df_sugerido['Cod Cliente_sugerido'] = df_sugerido['Cod Cliente_sugerido'].apply(lambda string: str(string).replace('nan', ''))
df_sugerido['Cod Cliente_sugerido'] = df_sugerido['Cod Cliente'] + df_sugerido['Cod Cliente_sugerido']

# junta as bases e exporta o resultado
df_03 = pd.merge(df, df_sugerido[['seq', 'Cod Cliente_sugerido', 'Nome_sugerido', 'DocId (11 digitos)_sugerido']], how='left', on=['seq'], suffixes=('', '') )
df_03.to_excel('tarefa_03.xlsx', index=False)

#########################
# Tarefa 02
#########################

# utiliza o DocId Sugerido
df_03.loc[df['DocId (11 digitos)'] == '00000000000', 'Cod Cliente'] = df_03['Cod Cliente_sugerido']
df_03.loc[df['DocId (11 digitos)'] == '00000000000', 'Nome'] = df_03['Nome_sugerido']
df_03.loc[df['DocId (11 digitos)'] == '00000000000', 'DocId (11 digitos)'] = df_03['DocId (11 digitos)_sugerido']

# Agrupa por Cod Cliente', 'DocId (11 digitos)
df_02 = df_03.groupby(['Cod Cliente', 'DocId (11 digitos)'], as_index = False).agg({'TIPO_LOGRADOURO': ';'.join, 'NOME_LOGRADOURO': ';'.join, 'NUMERO': ';'.join, 'COMPLEMENTO': ';'.join,})

df_02 = df_02.join(df_02['TIPO_LOGRADOURO'].str.split(';', expand=True).add_prefix('TIPO_LOGRADOURO_'))
df_02 = df_02.join(df_02['NOME_LOGRADOURO'].str.split(';', expand=True).add_prefix('NOME_LOGRADOURO_'))
df_02 = df_02.join(df_02['NUMERO'].str.split(';', expand=True).add_prefix('NUMERO_'))
df_02 = df_02.join(df_02['COMPLEMENTO'].str.split(';', expand=True).add_prefix('COMPLEMENTO_'))

# exporta resultado
df_02 = df_02.drop('TIPO_LOGRADOURO', axis=1)
df_02 = df_02.drop('NOME_LOGRADOURO', axis=1)
df_02 = df_02.drop('NUMERO', axis=1)
df_02 = df_02.drop('COMPLEMENTO', axis=1)
df_02.to_excel('tarefa_02.xlsx', index=False)
