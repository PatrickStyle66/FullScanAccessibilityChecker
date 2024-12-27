# FullScan Accessibility Checker
Um verificador de acessibilidade de varredura completa, ou seja, um verificador capaz de realizar a verificação de acessibilidade em todas as páginas de um website. A ferramenta consiste de três componentes principais: o web crawler que realiza a busca pelas páginas de um website, o avaliador que realiza a verificação de acessibilidade de cada página e a interface do usuário.

O processo de webcrawling e a coordenação do processo de análise são implementados através da ferramenta Selenium, que provê um webdriver para realizar o acesso e a interação com os websites, principalmente aqueles com conteúdo dinâmico. Durante o funcionamento da ferramenta, o webdriver dispõe de três abas no navegador para as quais são designadas funções específicas: a primeira aba é responsável por acessar a primeira página do website e porcurar por mais páginas, a segunda aba acessa o verificador Access Monitor e realiza a verificação de acessibilidade de páginas e , finalmente, a terceira página acessa as demais páginas encontradas na página inicial e continua o processo de busca por mais páginas.

Para o processo de localização e interação com os elementos das páginas web foram utilizadas consultas XPATH, que selecionam nós de um documento HTML através de filtros definidos nas consultas. Tais filtros, além de servirem para a localização dos elementos, servem para o descarte de links indesejáveis no processo de busca por páginas como links de redes sociais ou de elementos de mídia como fotos e vídeos, estes últimos não precisam ser analisados individualmente pois o verificador é capaz de analisá-los contidos na página.

A interface é implementada de maneira simples através do framework Streamlit , que facilita a visualização e interação com dados. Durante o processo de avaliação de páginas, as informações fornecidas pelo relatório de avaliação do Access Monitor são coletadas e armazenadas em um dataframe para posteriormente serem exibidas na interface do usuário, outras informações como as imagens geradas pelo relatório também compõem a exibição final da interface.

![FSAC](https://github.com/user-attachments/assets/1f82f8fb-9cf6-4b8c-bff6-fd7bcbfa297f)

## Módulos necessários
- Pandas
- Selenium
- Pyperclip
- Streamlit
- Requests

## Rodando o programa
Para iniciar a aplicação basta executar o comando `streamlit run FullScanChecker.py`.
