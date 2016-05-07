/**
 * John Collins, 10/4/2014
 *
 * This is a silly script containing random high-frequency functionality.
 */
var saveDataToMySQL = function(data) { // May not work. 
   var data_table = "hemisphere_dominance_study"; // change this for different experiments
   $.ajax({
      type:'post',
      cache: false,
      url: 'mysql_savedata.php',
      data: {
          table: data_table,
          json: JSON.stringify(data),
          opt_data: {key: value}
      },
      success: function(output) { console.log(output); } // write the result to javascript console
   });
}


var saveData = function(filename, filedata) {
            console.log("saving data")
            console.log(filename + " " + filedata)
            $.ajax({
                type:'post',
                cache: false,
                url: 'save_data.php', // this is the path to the above PHP script
                data: {filename: filename, filedata: filedata}
            });
        }


var fullscreen = function() { 
            if (screenfull.isFullscreen && $('#consent_checkbox').is(':checked')) {
                return true;
            } else {
                alert("If you with to participate, you must check the box next the the statement 'I agree to participate in this study.'");
                return false;
            }
        };


