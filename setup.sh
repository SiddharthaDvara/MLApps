@@ -1,9 +1,13 @@
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"siddartha.dronamraju@dvara.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
