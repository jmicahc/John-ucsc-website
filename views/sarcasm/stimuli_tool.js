/**
 * this is a tool for handling of stimuli.
 *
 */

var _getAllFilesFromFolder = function(dir) {

      var filesystem = require("fs");
      var results = [];

      filesystem.readdirSync(dir).forEach(function(file) {

          file = dir+'/'+file;
          var stat = filesystem.statSync(file);

          if (stat && stat.isDirectory()) {
              results = results.concat(_getAllFilesFromFolder(file))
          } else results.push(file);

    });

    return results;

};


var Stimuli = function(dir) {
  if (typeof path === 'undefined') path = 'Materials/';

  stimuli_paths = _getAllFilesFromFolder(dir);
  return stimuli_paths;
}


