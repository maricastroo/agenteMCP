from openpyxl import Workbook
import os

#⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄⠄⠂⠁⠁⠂⠄

ARQUIVO = "lista_compras.xlsx"

if not os.path.exists(ARQUIVO):
    wb = Workbook()
    ws = wb.active
    ws.append(["Produto"])
    wb.save(ARQUIVO)
    print("Planilha criada com sucesso!")
else:
    print("A planilha já existe.")