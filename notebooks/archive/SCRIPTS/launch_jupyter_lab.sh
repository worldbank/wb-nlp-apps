export XDG_RUNTIME_DIR=""
jupyter_lab_id=`pgrep jupyter-lab`
jupyter_lab_exit_status=$?
if [ $jupyter_lab_exit_status -eq 0 ]; then
    echo "jupyter-lab is running. killing pid $jupyter_lab_id ..."
    kill -15 $jupyter_lab_id
    echo "jupyter-lab killed ..."
fi
echo "running jupyter-lab ..."
source /home/wb536061/anaconda3/bin/activate
cd /R/NLP/
jupyter lab --ip="*" --port=1029 --NotebookApp.open_browser=False --LabApp.log_datefmt='%Y-%m-%d %H:%M:%S' >> jupyter.log 2>&1  & disown
echo "jupyter-lab now running detached. see jupyter.log for logs"
