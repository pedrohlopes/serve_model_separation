from flask import Flask, render_template, request, send_file
import subprocess
import os
app = Flask(__name__,static_url_path='')


@app.route('/upload')
def upload_file():
    return render_template('upload.html')
    
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file2():
    if request.method == 'POST':
        f = request.files['file']
        bashCommand = "python end-to-end.py u_net_3_7 " + f.filename +  " weights/best_3-7.hdf5"
        f.save(f.filename)
        #process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        #process.wait()
        basename = os.path.splitext(os.path.basename(f.filename))[0]
        final_filename = basename + "_vocals_pred.wav"
        print("audio/" + final_filename)
        return render_template('download.html', filename=final_filename)


@app.route('/downloader')
def download_file(filename):
    return send_file('audio/' + final_filename, as_attachment=True)
                                    
if __name__ == '__main__':
    app.run(port=8050)
