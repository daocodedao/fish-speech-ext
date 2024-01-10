. colors.sh


source venv_fish/bin/activate


jobName=tools.api_server:app
echo "${YELLOW}check $jobName pid ${NOCOLOR}"
echo "ps aux | grep "$jobName" | grep -v grep  | awk '{print $2}'"
TAILPID=`ps aux | grep "$jobName" | grep -v grep | awk '{print $2}'`
if [[ "0$TAILPID" != "0" ]]; then
echo "${RED}kill process $TAILPID${NOCOLOR}"
sudo kill -9 $TAILPID
fi

nohup python -m zibai tools.api_server:app --listen 127.0.0.1:8000  > /dev/null 2>&1 &


jobName=fish_speech/webui/app.py
echo "${YELLOW}check $jobName pid ${NOCOLOR}"
echo "ps aux | grep "$jobName" | grep -v grep "
TAILPID=`ps aux | grep "$jobName" | grep -v grep`
if [[ "0$TAILPID" != "0" ]]; then
echo "${RED}kill process $TAILPID${NOCOLOR}"
sudo kill -9 $TAILPID
fi

echo "${RED}python $jobName ${NOCOLOR}"

# GRADIO_SERVER_NAME=127.0.0.1 GRADIO_SERVER_PORT=5001 python app.py
# source venv_fish/bin/activate
# nohup GRADIO_SERVER_NAME=127.0.0.1 GRADIO_SERVER_PORT=5001 python fish_speech/webui/app.py > /dev/null 2>&1 & 

nohup python $jobName > /dev/null 2>&1 &


tail -f logs/api.log