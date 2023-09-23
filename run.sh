WORK_DIR=/root/workspace/telegram_gpt_bot

cd $WORK_DIR
echo $WORK_DIR
source $WORK_DIR/.venv/bin/activate


nohup python telegram_gpt_demo.py > $WORK_DIR/logs/run.log 2>&1 &

