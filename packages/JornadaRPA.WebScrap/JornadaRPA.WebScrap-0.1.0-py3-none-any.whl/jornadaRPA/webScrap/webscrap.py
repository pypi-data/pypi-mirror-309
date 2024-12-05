from botcity.web import *

import pandas


class Webscrap:
    def webscrap(self, inBot = '', inLines = '0', inNext = '', inXPATH = ''):
        # Assign Activity
        dados_linhas = []

        # Assign Activity
        exitRegister = False

        # Assign Activity
        registrosTotais = 0

        # While Activity
        while True:
            # Assign Activity
            colunas = [coluna.text for coluna in inBot.find_elements(selector= inXPATH + '//tr/th', by=By.XPATH)]

            # Assign Activity
            linhas_elementos = inBot.find_elements(selector= inXPATH + '//tr[not(.//th)]', by=By.XPATH)

            # Assign Activity
            registros = 0

            # ForEach Activity
            for linha in linhas_elementos:
                # Assign Activity
                celulas = linha.find_elements_by_xpath('.//td')

                # List Activity
                dados_linhas.append([celula.text for celula in celulas])

                # Assign Activity
                registros = registros + 1

                # Assign Activity
                registrosTotais = registrosTotais + 1

                # If Activity
                if inLines != 0:
                    # If Activity
                    if registrosTotais >= inLines:
                        # Assign Activity
                        exitRegister = True

                        # Break Activity
                        break




            # If Activity
            if not exitRegister:
                # Custom Python Code Activity
                inBot.scroll_down(registros)

                # Assign Activity
                proximo = inBot.find_element(selector=inNext, by=By.XPATH)

                # Try Activity
                try:
                    # Find And Click Activity
                    proximo.click()

                    # Custom Python Code Activity
                    inBot.scroll_up(registros)


                except Exception as ex:
                    # Break Activity
                    break



            # Else Activity
            else:
                # Break Activity
                break



        # Assign Activity
        outDatatable = pandas.DataFrame(dados_linhas, columns=colunas)


        return  outDatatable
