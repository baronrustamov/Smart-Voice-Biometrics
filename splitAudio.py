import subprocess
import os


def split_into_5(filename):
    try:
        train_list_txt = "train_user_audio_list.txt"
        test_list_txt = "test_user_audio_list.txt"
        curdir = os.getcwd()
        train_folder = "trainingData/{}/".format(filename)
        test_folder = "SampleData/{}".format(filename)
        out_path = "{}%03d.wav".format(filename)
        subprocess.call([
            'ffmpeg',
            '-i',
            filename,
            '-f',
            'segment',
            '-segment_time',
            '5',
            '-c',
            'copy',
            os.path.join(train_folder, out_path]
        )

        with open(os.path.join(curdir, train_list_txt), "w") as file:
            os.chdir(os.path.join(curdir, train_folder))
            train_list = os.listdir(os.getcwd())
            for item in train_list:
                file.write(item)
        file.close()

        with open(os.path.join(curdir, test_list_txt), "w") as file:
            os.chdir(os.path.join(curdir, test_folder))
            test_list = os.listdir(os.getcwd())
            for item in test_list:
                file.write(item)
        file.close()


        return 1
    except:
        return 0
