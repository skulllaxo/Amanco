values = ['90962', '1', 'DN 20 a 32', 'Pequena', '91361', '1', 'DN 40 a 63', 'Grande']
keys = ['CCB', 'Embalagem', 'Bitola', 'Tamanho']


rows = int(len(values)/len(keys))


f = str()
for i in range (0,rows):
    for j in range(0,len(keys)):
        f = f + keys[j]+': '+values[j+(len(keys)*i)]+' | '

    