package main

import (
	"fmt"
	"log"
	"net/http"
	"shotchart/shot"
)

const (
	anError = `<p class="error">%s</p>`
	pageTop = `<html>
  <head>
		<style>
			.chartWithOverlay {
	       position: relative;
	       width: 700px;
			 }
			.overlay {
	       width: 200px;
	       height: 200px;
	       position: absolute;
	       top: 0px;   /* chartArea top  */
	       left: 0px; /* chartArea left */
			 }
		</style>
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
			var data = new google.visualization.DataTable();
			data.addColumn('number', 'x') ;
      data.addColumn('number', 'y');
      data.addColumn(
        {type: 'string', role: 'tooltip'}
        );
				data.addRows([`
	/*   				 [ 8,      12],
	[ 4,      5.5],
	[ 11,     14],
	[ 4,      5],
	[ 3,      3.5],
	[ 6.5,    7]
	*/
	pageBottom = ` ]);

        var options = {
				backgroundColor: {fill: 'transparent'},
          title: 'James Harden shotchart',
          hAxis: {
						ticks: [-300,-150,0,150,300],
						baselineColor: 'none',
						gridlines: {
							color: 'none',
							count: '0',
							},
						textStyle: {
							color: 'none',
							},
						},
          vAxis: {
						ticks: [0,150,300],
						baselineColor: 'none',
						gridlines: {
							color: 'none',
							count: '0',
							},
						textStyle: {
		            color: 'none',
		          },
						},
          legend: 'none'
        };

        var chart = new google.visualization.ScatterChart(document.getElementById('chart_div'));

        chart.draw(data, options);
      }
    </script>

		<link rel="stylesheet" href="//code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
<script src="//code.jquery.com/jquery-1.10.2.js"></script>
<script src="//code.jquery.com/ui/1.11.4/jquery-ui.js"></script>
<link rel="stylesheet" href="/resources/demos/style.css">
<script>
$(function() {
	var availableTags = [
	"Quincy Acy","Jordan Adams","Steven Adams","Arron Afflalo","Dimitrios Agravanis","Alexis Ajinca","Furkan Aldemir","Cole Aldrich","LaMarcus Aldridge","Cliff Alexander","Lavoy Allen","Tony Allen","Al-Farouq Aminu","Lou Amundson","Chris Andersen","Alan Anderson","James Anderson","Justin Anderson","Kyle Anderson","Ryan Anderson","Giannis Antetokounmpo","Thanasis Antetokounmpo","Carmelo Anthony","Joel Anthony","Trevor Ariza","Darrell Arthur","Brandon Ashley","Omer Asik","D.J. Augustin","Chris Babb","Luke Babbitt","Cameron Bairstow","Leandro Barbosa","Jose Juan Barea","Andrea Bargnani","Harrison Barnes","Matt Barnes","Will Barton","Brandon Bass","Nicolas Batum","Jerryd Bayless","Aron Baynes","Kent Bazemore","Bradley Beal","Marco Belinelli","Anthony Bennett","Bismack Biyombo","Tarik Black","DeJuan Blair","Steve Blake","Eric Bledsoe","Ryan Boatright","Bojan Bogdanovic","Andrew Bogut","Matt Bonner","Devin Booker","Trevor Booker","Chris Bosh","Avery Bradley","Aaron Brooks","Anthony Brown","Jabari Brown","Lorenzo Brown","Markel Brown","Kobe Bryant","Chase Budinger","Reggie Bullock","Trey Burke","Alec Burks","Caron Butler","Jimmy Butler","Bruno Caboclo","Jose Calderon","Kentavious Caldwell-Pope","Isaiah Canaan","Clint Capela","DeMarre Carroll","Vince Carter","Michael Carter-Williams","Omri Casspi","Willie Cauley-Stein","Mario Chalmers","Tyson Chandler","Wilson Chandler","Rakeem Christmas","Jordan Clarkson","Darren Collison","Nick Collison","Mike Conley","Pat Connaughton","Jack Cooley","Chris Copeland","Bryce Cotton","DeMarcus Cousins","Robert Covington","Allen Crabbe","Jamal Crawford","Jae Crowder","Dante Cunningham","Seth Curry","Stephen Curry","Samuel Dalembert","Troy Daniels","Anthony Davis","Ed Davis","Branden Dawson","DeMar DeRozan","Dewayne Dedmon","Sam Dekker","Matthew Dellavedova","Luol Deng","Boris Diaw","Gorgui Dieng","Daniel Diez","Spencer Dinwiddie","Joey Dorsey","Goran Dragic","Andre Drummond","Jared Dudley","Duje Dukan","Tim Duncan","Mike Dunleavy","Kevin Durant","Cleanthony Early","Melvin Ejim","Wayne Ellington","Monta Ellis","Joel Embiid","James Ennis","Tyler Ennis","Marcus Eriksson","Jeremy Evans","Tyreke Evans","Dante Exum","Festus Ezeli","Jarrid Famous","Kenneth Faried","Derrick Favors","Cristiano Felicio","Raymond Felton","Evan Fournier","Randy Foye","Jamaal Franklin","Tim Frazier","Jimmer Fredette","Channing Frye","Danilo Gallinari","Langston Galloway","Kevin Garnett","Marc Gasol","Pau Gasol","Rudy Gay","Alonzo Gee","Paul George","Taj Gibson","Manu Ginobili","Rudy Gobert","Drew Gooden","Archie Goodwin","Aaron Gordon","Eric Gordon","Marcin Gortat","Danny Granger","Jerami Grant","Jerian Grant","Danny Green","Erick Green","Gerald Green","JaMychal Green","Jeff Green","Blake Griffin","Arturas Gudaitis","Jorge Gutierrez","PJ Hairston","Jordan Hamilton","Olivier Hanlan","Tyler Hansbrough","Tim Hardaway Jr.","James Harden","Maurice Harkless","Montrezl Harrell","Devin Harris","Gary Harris","Joe Harris","Tobias Harris","Aaron Harrison","Andrew Harrison","Tyler Harvey","Udonis Haslem","Spencer Hawes","Gordon Hayward","Gerald Henderson","John Henson","Guillermo Hernangomez","Mario Hezonja","Roy Hibbert","JJ Hickson"," Nene","George Hill","Jordan Hill","Solomon Hill","Darrun Hilliard","Kirk Hinrich","Jrue Holiday","Justin Holiday","Rondae Hollis-Jefferson","Richaun Holmes","Rodney Hood","Al Horford","Dwight Howard","Lester Hudson","Josh Huestis","Kris Humphries","RJ Hunter","Serge Ibaka","Andre Iguodala","Ersan Ilyasova","Joe Ingles","Damien Inglis","Kyrie Irving","Jarrett Jack","Reggie Jackson","LeBron James","Al Jefferson","Richard Jefferson","John Jenkins","Brandon Jennings","Jonas Jerebko","Grant Jerrett","Amir Johnson","Chris Johnson","Dakari Johnson","James Johnson","Joe Johnson","Nick Johnson","Stanley Johnson","Tyler Johnson","Wesley Johnson","Nikola Jokic","James Jones","Perry Jones","Terrence Jones","Tyus Jones","DeAndre Jordan","Cory Joseph","Chris Kaman","Frank Kaminsky","Enes Kanter","Sergey Karasev","Ryan Kelly","Michael Kidd-Gilchrist","Brandon Knight","Kyle Korver","Kosta Koufos","Zach LaVine","Cady Lalanne","Jeremy Lamb","Carl Landry","Shane Larkin","Joffrey Lauvergne","Ty Lawson","Courtney Lee","David Lee","Alex Len","Kawhi Leonard","Meyers Leonard","Jon Leuer","Damian Lillard","Jeremy Lin","Shaun Livingston","Kevon Looney","Brook Lopez","Robin Lopez","Kevin Love","Kyle Lowry","Trey Lyles","Shelvin Mack","Ian Mahinmi","Devyn Marble","Boban Marjanovic","Cartier Martin","Jarell Martin","Kevin Martin","Wesley Matthews","O.J. Mayo","James Michael McAdoo","Ray McCallum","CJ McCollum","Chris McCullough","Doug McDermott","Mitch McGary","Ben McLemore","Josh McRoberts","Jodie Meeks","Salah Mejri","Jordan Mickey","CJ Miles","Andre Miller","Mike Miller","Quincy Miller","Patty Mills","Elijah Millsap","Paul Millsap","Nikola Milutinov","Nikola Mirotic","Luka Mitrovic","Greg Monroe","Luis Montero","E'Twaun Moore","Marcus Morris","Markieff Morris","Anthony Morrow","Donatas Motiejunas","Timofey Mozgov","Emmanuel Mudiay","Shabazz Muhammad","Mike Muscala","Larry Nance Jr.","Shabazz Napier","Maurice Ndour","Gary Neal","Jameer Nelson","Andrew Nicholson","Joakim Noah","Nerlens Noel","Lucas Nogueira","Steve Novak","Dirk Nowitzki","Jusuf Nurkic","Johnny O'Bryant","Kyle O'Quinn","Jahlil Okafor","Victor Oladipo","Kelly Olynyk","Cedi Osman","Kelly Oubre","Zaza Pachulia","Kostas Papanikolaou","Jabari Parker","Tony Parker","Chandler Parsons","Lamar Patterson","Patrick Patterson","Chris Paul","Adreian Payne","Cameron Payne","Elfrid Payton","Nikola Pekovic","Kendrick Perkins","Terran Petteway","Paul Pierce","Mason Plumlee","Miles Plumlee","Sir'Dominic Pointer","Quincy Pondexter","Otto Porter","Bobby Portis","Kristaps Porzingis","Dwight Powell","Norman Powell","Phil Pressey","Ronnie Price","Pablo Prigioni","Nikola Radicevic","Julius Randle","Zach Randolph","JJ Redick","Willie Reed","Josh Richardson","Austin Rivers","Andre Roberson","Brian Roberts","Glenn Robinson","Thomas Robinson","Rajon Rondo","Derrick Rose","Terrence Ross","Terry Rozier","Ricky Rubio","Damjan Rudez","Brandon Rush","D'Angelo Russell","Robert Sacre","JaKarr Sampson","Dennis Schroder","Luis Scola","Mike Scott","Thabo Sefolosha","Kevin Seraphin","Ramon Sessions","Iman Shumpert","Jonathan Simmons","Satnam Singh","Kyle Singler","Donald Sloan","Marcus Smart","Jason Smith","Josh Smith","Russ Smith","Tony Snell","Marreese Speights","Tiago Splitter","Nik Stauskas","Lance Stephenson","David Stockton","Jarnell Stokes","Amar'e Stoudemire","Rodney Stuckey","Jared Sullinger","Walter Tavares","Jeff Teague","Mirza Teletovic","Adonis Thomas","Isaiah Thomas","Lance Thomas","Hollis Thompson","Jason Thompson","Klay Thompson","Marcus Thornton","JP Tokoto","Anthony Tolliver","Karl-Anthony Towns","PJ Tucker","Evan Turner","Myles Turner","Beno Udrih","Jonas Valanciunas","Anderson Varejao","Greivis Vasquez","Rashad Vaughn","Juan Pablo Vaulet","Charlie Villanueva","Noah Vonleh","Nikola Vucevic","Sasha Vujacic","Dwyane Wade","Dion Waiters","Kemba Walker","John Wall","Gerald Wallace","TJ Warren","CJ Watson","Martell Webster","Sonny Weems","David West","Russell Westbrook","Aaron White","Hassan Whiteside","Shayne Whittington","Andrew Wiggins","CJ Wilcox","Deron Williams","Derrick Williams","Lou Williams","Marvin Williams","Mo Williams","Reggie Williams","Jamil Wilson","Justise Winslow","Brandan Wright","Delon Wright","Tony Wroten","James Young","Joe Young","Nick Young","Thaddeus Young","Cody Zeller","Tyler Zeller"
	];
	$( "#names" ).autocomplete({
		source: availableTags
	});
});

</script>
</head>

  <body>
	<div class="chartWithOverlay">
    <div class="overlay">
     <img src="http://images.clipartpanda.com/basketball-half-court-clipart-yikerABpT.jpeg" height=400px>
   </div>
   <div id="chart_div" style="width: 800px; height: 400px;"></div>
 </div>

 <form action="/" method="POST">
	<div class="ui-widget">
	<label for="names">Search:</label><br />
	<input type="text" name="names" id="names" size="30"><br />
	<input type="submit" value="Submit">
	</div>
	</form>

</body>
</html>`
)

func main() {
	http.HandleFunc("/", homePage)
	if err := http.ListenAndServe(":9001", nil); err != nil {
		log.Fatal("failed to start server", err)
	}
}

func processRequest(request *http.Request) {
	player := request.Form["names"]
	fmt.Println("Player is", player)
}

func homePage(writer http.ResponseWriter, request *http.Request) {
	err := request.ParseForm()
	if err != nil {
		fmt.Fprintf(writer, anError, err)
	}
	array := "[-64, 33, '7 feet'],[-46, 26, '5 feet'],[0, 1, '0 feet'],[-10, 17, '1 feet'],[1, 67, '6 feet'],[-82, 244, '25 feet'],[222, 124, '25 feet'],[177, 175, '24 feet'],[144, 254, '29 feet'],[-10, 53, '5 feet'],[140, 217, '25 feet'],[-103, 217, '24 feet'],[97, 178, '20 feet'],[-23, 47, '5 feet'],[0, 58, '5 feet'],[2, 247, '24 feet'],[-8, -2, '0 feet'],[-4, 12, '1 feet'],[-21, 17, '2 feet'],[-43, 51, '6 feet'],[-32, 19, '3 feet'],[-64, 89, '10 feet'],[-64, 244, '25 feet'],[0, 140, '14 feet'],[-93, 255, '27 feet'],[31, 17, '3 feet'],[-10, 12, '1 feet'],[193, 157, '24 feet'],[-84, 231, '24 feet'],[-8, -10, '1 feet'],[0, 160, '16 feet'],[-11, 12, '1 feet'],[-19, 242, '24 feet'],[162, 186, '24 feet'],[0, 9, '0 feet'],[-11, 0, '1 feet'],[12, -8, '1 feet'],[-5, 12, '1 feet'],[125, 205, '24 feet'],[-2, 9, '0 feet'],[-108, 89, '13 feet'],[94, 148, '17 feet'],[0, -2, '0 feet'],[-32, 15, '3 feet'],[24, 113, '11 feet'],[100, 58, '11 feet'],[196, 162, '25 feet'],[34, 46, '5 feet'],[-163, 197, '25 feet'],[-7, 271, '27 feet'],[217, 124, '24 feet'],[-11, 0, '1 feet'],[-2, 11, '1 feet'],[-49, 246, '25 feet'],[-175, 190, '25 feet'],[124, 131, '18 feet'],[-240, 118, '26 feet'],[-128, 93, '15 feet'],[-19, 258, '25 feet'],[-2, 19, '1 feet'],[-235, 86, '25 feet'],[10, 15, '1 feet'],[-8, 45, '4 feet'],[-11, -1, '1 feet'],[-174, 184, '25 feet'],[-7, 7, '0 feet'],[-10, 156, '15 feet'],[23, 3, '2 feet'],[201, 168, '26 feet'],[-16, 1, '1 feet'],[-40, 198, '20 feet'],[0, 25, '2 feet'],[-19, -5, '1 feet'],[136, 216, '25 feet'],[225, 115, '25 feet'],[92, 235, '25 feet'],[-13, 6, '1 feet'],[-40, 6, '4 feet'],[-158, 127, '20 feet'],[-16, 131, '13 feet'],[32, 190, '19 feet'],[0, 1, '0 feet'],[31, 11, '3 feet'],[62, 113, '12 feet'],[17, 20, '2 feet'],[230, 15, '23 feet'],[198, 159, '25 feet'],[195, 159, '25 feet'],[168, 131, '21 feet'],[-13, 1, '1 feet'],[95, 113, '14 feet'],[-13, 3, '1 feet'],[-232, 6, '23 feet'],[-37, -11, '3 feet'],[23, 20, '3 feet'],[-90, 168, '19 feet'],[-117, 55, '12 feet'],[1, 268, '26 feet'],[-14, 19, '2 feet'],[-13, 25, '2 feet'],[-111, 138, '17 feet'],[0, 246, '24 feet'],[-234, 22, '23 feet'],[24, 12, '2 feet'],[220, 123, '25 feet'],[-21, 0, '2 feet'],[58, 142, '15 feet'],[13, -2, '1 feet'],[-8, 12, '1 feet'],[13, 4, '1 feet'],[-120, 222, '25 feet'],[-103, 165, '19 feet'],[135, 209, '24 feet'],[-234, -17, '23 feet'],[1, 345, '34 feet'],[-18, 9, '2 feet'],[222, 71, '23 feet'],[157, 190, '24 feet'],[6, 6, '0 feet'],[0, 1, '0 feet'],[223, 101, '24 feet'],[-46, 239, '24 feet'],[-199, 160, '25 feet'],[-32, 93, '9 feet'],[80, 192, '20 feet'],[-52, 64, '8 feet'],[0, 1, '0 feet'],[-19, 0, '1 feet'],[78, 236, '24 feet'],[102, 222, '24 feet'],[111, 216, '24 feet'],[-131, 217, '25 feet'],[99, 149, '17 feet'],[17, 55, '5 feet'],[-81, 236, '24 feet'],[0, 255, '25 feet'],[-48, 194, '19 feet'],[0, 242, '24 feet'],[-7, 3, '0 feet'],[4, 190, '19 feet'],[-144, 200, '24 feet'],[-10, 246, '24 feet'],[-142, 47, '14 feet'],[1, 4, '0 feet'],[-57, 236, '24 feet'],[154, 187, '24 feet'],[-215, 107, '24 feet'],[1, 9, '0 feet'],[130, 113, '17 feet'],[7, -11, '1 feet'],[-174, 175, '24 feet'],[88, 244, '25 feet'],[-138, 149, '20 feet'],[-15, 63, '6 feet'],[-37, 230, '23 feet'],[105, 118, '15 feet'],[162, 190, '24 feet'],[-146, 203, '25 feet'],[64, 63, '8 feet'],[0, -6, '0 feet'],[1, 6, '0 feet'],[-4, 0, '0 feet'],[23, 280, '28 feet'],[-5, 12, '1 feet'],[-105, 123, '16 feet'],[-97, 228, '24 feet'],[-127, 220, '25 feet'],[9, 26, '2 feet'],[-46, 263, '26 feet'],[0, 1, '0 feet'],[100, 236, '25 feet'],[20, 246, '24 feet'],[0, 4, '0 feet'],[-11, 170, '17 feet'],[223, 104, '24 feet'],[143, 85, '16 feet'],[-228, 23, '22 feet'],[-41, 238, '24 feet'],[159, 197, '25 feet'],[0, 39, '3 feet'],[141, 220, '26 feet'],[17, 242, '24 feet'],[119, -6, '11 feet'],[12, 11, '1 feet'],[-13, 1, '1 feet'],[-182, 165, '24 feet'],[-2, 42, '4 feet'],[-21, 22, '3 feet'],[29, 12, '3 feet'],[1, 0, '0 feet'],[6, 42, '4 feet'],[-112, 148, '18 feet'],[-112, 153, '18 feet'],[-16, 23, '2 feet'],[97, 181, '20 feet'],[65, 86, '10 feet'],[-90, 86, '12 feet'],[-21, 7, '2 feet'],[-11, 9, '1 feet'],[-65, 239, '24 feet'],[-14, 8, '1 feet'],[89, 230, '24 feet'],[-112, 225, '25 feet'],[-81, 4, '8 feet'],[-7, 6, '0 feet'],[0, 107, '10 feet'],[-185, 189, '26 feet'],[24, 0, '2 feet'],[-64, 42, '7 feet'],[-4, -2, '0 feet'],[56, 252, '25 feet'],[185, 167, '24 feet'],[0, -10, '1 feet'],[0, 6, '0 feet'],[-125, 216, '24 feet'],[36, 142, '14 feet'],[20, 0, '2 feet'],[-11, -2, '1 feet'],[0, 4, '0 feet'],[125, 124, '17 feet'],[-93, 165, '18 feet'],[-141, 129, '19 feet'],[-120, 222, '25 feet'],[48, 247, '25 feet'],[0, 3, '0 feet'],[-2, 33, '3 feet'],[51, 153, '16 feet'],[211, 132, '24 feet'],[4, 208, '20 feet'],[228, 15, '22 feet'],[-52, 244, '24 feet'],[149, 192, '24 feet'],[-152, 30, '15 feet'],[-41, 15, '4 feet'],[-122, 211, '24 feet'],[12, -10, '1 feet'],[-21, 255, '25 feet'],[121, 189, '22 feet'],[159, 194, '25 feet'],[-133, 99, '16 feet'],[106, 217, '24 feet'],[67, 44, '8 feet'],[1, 244, '24 feet'],[100, 77, '12 feet'],[6, 75, '7 feet'],[4, -8, '0 feet'],[102, 224, '24 feet'],[3, 0, '0 feet'],[130, 211, '24 feet'],[34, 86, '9 feet'],[-8, -2, '0 feet'],[6, 246, '24 feet'],[-152, 184, '23 feet'],[13, 0, '1 feet'],[9, 261, '26 feet'],[-81, 140, '16 feet'],[116, 173, '20 feet'],[83, 238, '25 feet'],[24, 242, '24 feet'],[26, 241, '24 feet'],[0, 6, '0 feet'],[-89, 131, '15 feet'],[0, 1, '0 feet'],[-18, 14, '2 feet'],[237, 26, '23 feet'],[59, 96, '11 feet'],[99, 108, '14 feet'],[1, 19, '1 feet'],[9, 14, '1 feet'],[-105, 249, '27 feet'],[7, 1, '0 feet'],[-90, 55, '10 feet'],[138, 11, '13 feet'],[-4, -2, '0 feet'],[-5, -6, '0 feet'],[241, 41, '24 feet'],[168, 186, '25 feet'],[-35, 25, '4 feet'],[-146, 206, '25 feet'],[-160, 187, '24 feet'],[6, 1, '0 feet'],[-237, 39, '24 feet'],[94, 77, '12 feet'],[184, 170, '25 feet'],[36, 247, '24 feet'],[-10, 12, '1 feet'],[234, 137, '27 feet'],[168, -16, '16 feet'],[-4, 12, '1 feet'],[105, 135, '17 feet'],[-123, 220, '25 feet'],[-5, 0, '0 feet'],[-202, 138, '24 feet'],[-191, 160, '24 feet'],[6, 176, '17 feet'],[12, 266, '26 feet'],[-13, -5, '1 feet'],[122, 121, '17 feet'],[-26, 250, '25 feet'],[4, 0, '0 feet'],[-235, -14, '23 feet'],[-8, -10, '1 feet'],[-57, 159, '16 feet'],[214, 131, '25 feet'],[20, 254, '25 feet'],[-86, 119, '14 feet'],[0, 1, '0 feet'],[-7, 6, '0 feet'],[-183, 181, '25 feet'],[-163, 189, '24 feet'],[20, 0, '2 feet'],[130, 222, '25 feet'],[-153, 194, '24 feet'],[65, 197, '20 feet'],[-98, 236, '25 feet'],[-51, 160, '16 feet'],[-10, 9, '1 feet'],[-35, 7, '3 feet'],[114, 94, '14 feet'],[103, 220, '24 feet'],[193, -8, '19 feet'],[-149, 194, '24 feet'],[-131, 112, '17 feet'],[125, 209, '24 feet'],[81, 233, '24 feet'],[157, -24, '15 feet'],[155, 194, '24 feet'],[-54, 181, '18 feet'],[-48, 22, '5 feet'],[-32, 22, '3 feet'],[12, 19, '2 feet'],[24, 23, '3 feet'],[4, 89, '8 feet'],[-19, 1, '1 feet'],[-209, 11, '20 feet'],[-10, 42, '4 feet'],[-108, 227, '25 feet'],[-4, 15, '1 feet'],[10, 7, '1 feet'],[-46, 173, '17 feet'],[-13, 7, '1 feet'],[162, 14, '16 feet'],[174, 36, '17 feet'],[-18, 11, '2 feet'],[69, 189, '20 feet'],[181, 165, '24 feet'],[-21, 249, '24 feet'],[-46, 246, '25 feet'],[-8, 22, '2 feet'],[-146, 135, '19 feet'],[-232, 110, '25 feet'],[-15, 15, '2 feet'],"
	data := array

	processRequest(request)
	shotData := shot.GetShots(3243)
	for _, shot := range shotData {
		data := fmt.Sprint("[", shot.LocationX, ", ", shot.LocationY, ", ", "'", shot.ShotDistance, " feet", "'", "],", data)
	}

	fmt.Fprint(writer, pageTop, data, pageBottom)

}
