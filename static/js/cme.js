$(function(){
var stateOptions;
	$.getJSON('D:/MCA_Django_Project/guestworker/static/js/countries.json',function(result){
		$.each(result, function(i,state) {
			//<option value='countrycode'>contryname</option>
			stateOptions+="<option value='"
			+state.code+
			"'>"
			+state.name+
			"</option>";
			 });
			 $('#state').html(stateOptions);
	});
});
