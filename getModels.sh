mkdir models
wget https://github.com/richzhang/colorization/blob/8aa25ac7b6215bf6789e682b6fa3433164d4a3a4/resources/pts_in_hull.npy -O ./pts_in_hull.npy
wget https://raw.githubusercontent.com/alexellis/faas-colorization/master/function/models/colorization_deploy_v2.prototxt -O ./models/colorization_deploy_v2.prototxt
wget http://people.eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2.caffemodel -O ./models/colorization_release_v2.caffemodel
wget http://people.eecs.berkeley.edu/~rich.zhang/projects/2016_colorization/files/demo_v2/colorization_release_v2_norebal.caffemodel -O ./models/colorization_release_v2_norebal.caffemodel
