import React, { Component } from "react";

class WahlkreisZweit extends Component {
  state = {
    value: 1,
  };
  render() {
    return (
      <React.Fragment>
        <h2>Wahlkreisubersicht</h2>
        <select
          defaultValue={1}
          onChange={this.handleValue}
          id="wahlkreis_choice"
        >
          <option value="1">Flensburg – Schleswig</option>
          <option value="2">Nordfriesland – Dithmarschen Nord</option>
          <option value="3">Steinburg – Dithmarschen Süd</option>
          <option value="4">Rendsburg-Eckernförde</option>
          <option value="5">Kiel</option>
          <option value="6">Plön – Neumünster</option>
          <option value="7">Pinneberg</option>
          <option value="8">Segeberg – Stormarn-Mitte</option>
          <option value="9">Ostholstein – Stormarn-Nord</option>
          <option value="10">Herzogtum Lauenburg – Stormarn-Süd</option>
          <option value="11">Lübeck</option>
          <option value="12">
            Schwerin – Ludwigslust-Parchim I – Nordwestmecklenburg I
          </option>
          <option value="13">
            Ludwigslust-Parchim II – Nordwestmecklenburg II – Landkreis Rostock
            I
          </option>
          <option value="14">Rostock – Landkreis Rostock II</option>
          <option value="15">Vorpommern-Rügen – Vorpommern-Greifswald I</option>
          <option value="16">
            Mecklenburgische Seenplatte I – Vorpommern-Greifswald II
          </option>
          <option value="17">
            Mecklenburgische Seenplatte II – Landkreis Rostock III
          </option>
          <option value="18">Hamburg-Mitte</option>
          <option value="19">Hamburg-Altona</option>
          <option value="20">Hamburg-Eimsbüttel</option>
          <option value="21">Hamburg-Nord</option>
          <option value="22">Hamburg-Wandsbek</option>
          <option value="23">Hamburg-Bergedorf – Harburg</option>
          <option value="24">Aurich – Emden</option>
          <option value="25">Unterems</option>
          <option value="26">Friesland – Wilhelmshaven – Wittmund</option>
          <option value="27">Oldenburg – Ammerland</option>
          <option value="28">Delmenhorst – Wesermarsch – Oldenburg-Land</option>
          <option value="29">Cuxhaven – Stade II</option>
          <option value="30">Stade I – Rotenburg II</option>
          <option value="31">Mittelems</option>
          <option value="32">Cloppenburg – Vechta</option>
          <option value="33">Diepholz – Nienburg I</option>
          <option value="34">Osterholz – Verden</option>
          <option value="35">Rotenburg I – Heidekreis</option>
          <option value="36">Harburg</option>
          <option value="37">Lüchow-Dannenberg – Lüneburg</option>
          <option value="38">Osnabrück-Land</option>
          <option value="39">Stadt Osnabrück</option>
          <option value="40">Nienburg II – Schaumburg</option>
          <option value="41">Stadt Hannover I</option>
          <option value="42">Stadt Hannover II</option>
          <option value="43">Hannover-Land I</option>
          <option value="44">Celle – Uelzen</option>
          <option value="45">Gifhorn – Peine</option>
          <option value="46">Hameln-Pyrmont – Holzminden</option>
          <option value="47">Hannover-Land II</option>
          <option value="48">Hildesheim</option>
          <option value="49">Salzgitter – Wolfenbüttel</option>
          <option value="50">Braunschweig</option>
          <option value="51">Helmstedt – Wolfsburg</option>
          <option value="52">Goslar – Northeim – Osterode</option>
          <option value="53">Göttingen</option>
          <option value="54">Bremen I</option>
          <option value="55">Bremen II – Bremerhaven</option>
          <option value="56">
            Prignitz – Ostprignitz-Ruppin – Havelland I
          </option>
          <option value="57">Uckermark – Barnim I</option>
          <option value="58">Oberhavel – Havelland II</option>
          <option value="59">Märkisch-Oderland – Barnim II</option>
          <option value="60">
            Brandenburg an der Havel – Potsdam-Mittelmark I – Havelland III –
            Teltow-Fläming I
          </option>
          <option value="61">
            Potsdam – Potsdam-Mittelmark II – Teltow-Fläming II
          </option>
          <option value="62">
            Dahme-Spreewald – Teltow-Fläming III – Oberspreewald-Lausitz I
          </option>
          <option value="63">Frankfurt (Oder) – Oder-Spree</option>
          <option value="64">Cottbus – Spree-Neiße</option>
          <option value="65">Elbe-Elster – Oberspreewald-Lausitz II</option>
          <option value="66">Altmark</option>
          <option value="67">Börde – Jerichower Land</option>
          <option value="68">Harz</option>
          <option value="69">Magdeburg</option>
          <option value="70">Dessau – Wittenberg</option>
          <option value="71">Anhalt</option>
          <option value="72">Halle</option>
          <option value="73">Burgenland – Saalekreis</option>
          <option value="74">Mansfeld</option>
          <option value="75">Berlin-Mitte</option>
          <option value="76">Berlin-Pankow</option>
          <option value="77">Berlin-Reinickendorf</option>
          <option value="78">Berlin-Spandau – Charlottenburg Nord</option>
          <option value="79">Berlin-Steglitz-Zehlendorf</option>
          <option value="80">Berlin-Charlottenburg-Wilmersdorf</option>
          <option value="81">Berlin-Tempelhof-Schöneberg</option>
          <option value="82">Berlin-Neukölln</option>
          <option value="83">
            Berlin-Friedrichshain-Kreuzberg – Prenzlauer Berg Ost
          </option>
          <option value="84">Berlin-Treptow-Köpenick</option>
          <option value="85">Berlin-Marzahn-Hellersdorf</option>
          <option value="86">Berlin-Lichtenberg</option>
          <option value="87">Aachen I</option>
          <option value="88">Aachen II</option>
          <option value="89">Heinsberg</option>
          <option value="90">Düren</option>
          <option value="91">Rhein-Erft-Kreis I</option>
          <option value="92">Euskirchen – Rhein-Erft-Kreis II</option>
          <option value="93">Köln I</option>
          <option value="94">Köln II</option>
          <option value="95">Köln III</option>
          <option value="96">Bonn</option>
          <option value="97">Rhein-Sieg-Kreis I</option>
          <option value="98">Rhein-Sieg-Kreis II</option>
          <option value="99">Oberbergischer Kreis</option>
          <option value="100">Rheinisch-Bergischer Kreis</option>
          <option value="101">Leverkusen – Köln IV</option>
          <option value="102">Wuppertal I</option>
          <option value="103">Solingen – Remscheid – Wuppertal II</option>
          <option value="104">Mettmann I</option>
          <option value="105">Mettmann II</option>
          <option value="106">D�sseldorf I</option>
          <option value="107">Düsseldorf II</option>
          <option value="108">Neuss I</option>
          <option value="109">Mönchengladbach</option>
          <option value="110">Krefeld I – Neuss II</option>
          <option value="111">Viersen</option>
          <option value="112">Kleve</option>
          <option value="113">Wesel I</option>
          <option value="114">Krefeld II – Wesel II</option>
          <option value="115">Duisburg I</option>
          <option value="116">Duisburg II</option>
          <option value="117">Oberhausen – Wesel III</option>
          <option value="118">Mülheim – Essen I</option>
          <option value="119">Essen II</option>
          <option value="120">Essen III</option>
          <option value="121">Recklinghausen I</option>
          <option value="122">Recklinghausen II</option>
          <option value="123">Gelsenkirchen</option>
          <option value="124">Steinfurt I – Borken I</option>
          <option value="125">Bottrop – Recklinghausen III</option>
          <option value="126">Borken II</option>
          <option value="127">Coesfeld – Steinfurt II</option>
          <option value="128">Steinfurt III</option>
          <option value="129">Münster</option>
          <option value="130">Warendorf</option>
          <option value="131">Gütersloh I</option>
          <option value="132">Bielefeld – Gütersloh II</option>
          <option value="133">Herford – Minden-Lübbecke II</option>
          <option value="134">Minden-Lübbecke I</option>
          <option value="135">Lippe I</option>
          <option value="136">Höxter – Gütersloh III – Lippe II</option>
          <option value="137">Paderborn</option>
          <option value="138">Hagen – Ennepe-Ruhr-Kreis I</option>
          <option value="139">Ennepe-Ruhr-Kreis II</option>
          <option value="140">Bochum I</option>
          <option value="141">Herne – Bochum II</option>
          <option value="142">Dortmund I</option>
          <option value="143">Dortmund II</option>
          <option value="144">Unna I</option>
          <option value="145">Hamm – Unna II</option>
          <option value="146">Soest</option>
          <option value="147">Hochsauerlandkreis</option>
          <option value="148">Siegen-Wittgenstein</option>
          <option value="149">Olpe – Märkischer Kreis I</option>
          <option value="150">Märkischer Kreis II</option>
          <option value="151">Nordsachsen</option>
          <option value="152">Leipzig I</option>
          <option value="153">Leipzig II</option>
          <option value="154">Leipzig-Land</option>
          <option value="155">Meißen</option>
          <option value="156">Bautzen I</option>
          <option value="157">Görlitz</option>
          <option value="158">Sächsische Schweiz-Osterzgebirge</option>
          <option value="159">Dresden I</option>
          <option value="160">Dresden II – Bautzen II</option>
          <option value="161">Mittelsachsen</option>
          <option value="162">Chemnitz</option>
          <option value="163">Chemnitzer Umland – Erzgebirgskreis II</option>
          <option value="164">Erzgebirgskreis I</option>
          <option value="165">Zwickau</option>
          <option value="166">Vogtlandkreis</option>
          <option value="167">Waldeck</option>
          <option value="168">Kassel</option>
          <option value="169">Werra-Meißner – Hersfeld-Rotenburg</option>
          <option value="170">Schwalm-Eder</option>
          <option value="171">Marburg</option>
          <option value="172">Lahn-Dill</option>
          <option value="173">Gießen</option>
          <option value="174">Fulda</option>
          <option value="175">Main-Kinzig – Wetterau II – Schotten</option>
          <option value="176">Hochtaunus</option>
          <option value="177">Wetterau I</option>
          <option value="178">Rheingau-Taunus – Limburg</option>
          <option value="179">Wiesbaden</option>
          <option value="180">Hanau</option>
          <option value="181">Main-Taunus</option>
          <option value="182">Frankfurt am Main I</option>
          <option value="183">Frankfurt am Main II</option>
          <option value="184">Groß-Gerau</option>
          <option value="185">Offenbach</option>
          <option value="186">Darmstadt</option>
          <option value="187">Odenwald</option>
          <option value="188">Bergstraße</option>
          <option value="189">Eichsfeld – Nordhausen – Kyffhäuserkreis</option>
          <option value="190">
            Eisenach – Wartburgkreis – Unstrut-Hainich-Kreis
          </option>
          <option value="191">Jena �� Sömmerda – Weimarer Land I</option>
          <option value="192">Gotha – Ilm-Kreis</option>
          <option value="193">Erfurt – Weimar – Weimarer Land II</option>
          <option value="194">Gera – Greiz – Altenburger Land</option>
          <option value="195">
            Saalfeld-Rudolstadt – Saale-Holzland-Kreis – Saale-Orla-Kreis
          </option>
          <option value="196">
            Suhl – Schmalkalden-Meiningen – Hildburghausen – Sonneberg
          </option>
          <option value="197">Neuwied</option>
          <option value="198">Ahrweiler</option>
          <option value="199">Koblenz</option>
          <option value="200">Mosel/Rhein-Hunsrück</option>
          <option value="201">Kreuznach</option>
          <option value="202">Bitburg</option>
          <option value="203">Trier</option>
          <option value="204">Montabaur</option>
          <option value="205">Mainz</option>
          <option value="206">Worms</option>
          <option value="207">Ludwigshafen/Frankenthal</option>
          <option value="208">Neustadt – Speyer</option>
          <option value="209">Kaiserslautern</option>
          <option value="210">Pirmasens</option>
          <option value="211">Südpfalz</option>
          <option value="212">Altötting</option>
          <option value="213">Erding – Ebersberg</option>
          <option value="214">Freising</option>
          <option value="215">Fürstenfeldbruck</option>
          <option value="216">Ingolstadt</option>
          <option value="217">München-Nord</option>
          <option value="218">München-Ost</option>
          <option value="219">München-Süd</option>
          <option value="220">München-West/Mitte</option>
          <option value="221">München-Land</option>
          <option value="222">Rosenheim</option>
          <option value="223">Bad Tölz-Wolfratshausen – Miesbach</option>
          <option value="224">Starnberg – Landsberg am Lech</option>
          <option value="225">Traunstein</option>
          <option value="226">Weilheim</option>
          <option value="227">Deggendorf</option>
          <option value="228">Landshut</option>
          <option value="229">Passau</option>
          <option value="230">Rottal-Inn</option>
          <option value="231">Straubing</option>
          <option value="232">Amberg</option>
          <option value="233">Regensburg</option>
          <option value="234">Schwandorf</option>
          <option value="235">Weiden</option>
          <option value="236">Bamberg</option>
          <option value="237">Bayreuth</option>
          <option value="238">Coburg</option>
          <option value="239">Hof</option>
          <option value="240">Kulmbach</option>
          <option value="241">Ansbach</option>
          <option value="242">Erlangen</option>
          <option value="243">Fürth</option>
          <option value="244">Nürnberg-Nord</option>
          <option value="245">Nürnberg-Süd</option>
          <option value="246">Roth</option>
          <option value="247">Aschaffenburg</option>
          <option value="248">Bad Kissingen</option>
          <option value="249">Main-Spessart</option>
          <option value="250">Schweinfurt</option>
          <option value="251">Würzburg</option>
          <option value="252">Augsburg-Stadt</option>
          <option value="253">Augsburg-Land</option>
          <option value="254">Donau-Ries</option>
          <option value="255">Neu-Ulm</option>
          <option value="256">Oberallgäu</option>
          <option value="257">Ostallgäu</option>
          <option value="258">Stuttgart I</option>
          <option value="259">Stuttgart II</option>
          <option value="260">Böblingen</option>
          <option value="261">Esslingen</option>
          <option value="262">Nürtingen</option>
          <option value="263">Göppingen</option>
          <option value="264">Waiblingen</option>
          <option value="265">Ludwigsburg</option>
          <option value="266">Neckar-Zaber</option>
          <option value="267">Heilbronn</option>
          <option value="268">Schwäbisch Hall – Hohenlohe</option>
          <option value="269">Backnang – Schwäbisch Gmünd</option>
          <option value="270">Aalen – Heidenheim</option>
          <option value="271">Karlsruhe-Stadt</option>
          <option value="272">Karlsruhe-Land</option>
          <option value="273">Rastatt</option>
          <option value="274">Heidelberg</option>
          <option value="275">Mannheim</option>
          <option value="276">Odenwald – Tauber</option>
          <option value="277">Rhein-Neckar</option>
          <option value="278">Bruchsal – Schwetzingen</option>
          <option value="279">Pforzheim</option>
          <option value="280">Calw</option>
          <option value="281">Freiburg</option>
          <option value="282">Lörrach – Müllheim</option>
          <option value="283">Emmendingen – Lahr</option>
          <option value="284">Offenburg</option>
          <option value="285">Rottweil – Tuttlingen</option>
          <option value="286">Schwarzwald-Baar</option>
          <option value="287">Konstanz</option>
          <option value="288">Waldshut</option>
          <option value="289">Reutlingen</option>
          <option value="290">Tübingen</option>
          <option value="291">Ulm</option>
          <option value="292">Biberach</option>
          <option value="293">Bodensee</option>
          <option value="294">Ravensburg</option>
          <option value="295">Zollernalb – Sigmaringen</option>
          <option value="296">Saarbrücken</option>
          <option value="297">Saarlouis</option>
          <option value="298">St. Wendel</option>
          <option value="299">Homburg</option>
        </select>
        <h3>Wahlbeteiligung</h3>
        <div id="Wahlbeteiligung">
          <h4>2021: </h4>
          <p style={{ paddingLeft: "40px" }} id="wahlbet"></p>
          {this.renderTable1()}
          <h4>2017: </h4>
          <p style={{ paddingLeft: "40px" }} id="wahlbet2017"></p>
          {this.renderTable12017()}
        </div>

        <h3>Direktkandidaten</h3>
        <div id="direkt">
          <div id="Direktkandidaten_info">
            <h4>2021: </h4>
            <p style={{ paddingLeft: "40px" }} id="direktkand"></p>
            {this.renderTable2()}
            <h4>2017: </h4>
            <p style={{ paddingLeft: "40px" }} id="direktkand2017"></p>
            {this.renderTable22017()}
          </div>
        </div>

        <h3>Pro Partei, entwicklung</h3>
        <div id="partei_entw">
          <table id="p_entw"></table>
          {this.renderTable3()}
        </div>
      </React.Fragment>
    );
  }

  handleValue = () => {
    var menu = document.getElementById("wahlkreis_choice");
    this.setState({ value: menu.value });
    // console.log(this.state.value);
  };

  handlereq12017() {
    fetch(
      "http://localhost:8000/query3_wahlbeteiligung2017/" +
        this.state.value.toString()
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("p");
        var tag_id = document.getElementById("wahlbet2017");
        tag_id.innerHTML = data["data"];
        // console.log(this.state.value.toString());
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }
  renderTable12017() {
    return this.handlereq12017();
  }

  handlereq1() {
    fetch(
      "http://localhost:8000/query3_wahlbeteiligung/" +
        this.state.value.toString()
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("p");
        var tag_id = document.getElementById("wahlbet");
        tag_id.innerHTML = data["data"];
        // console.log(this.state.value.toString());
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }
  renderTable1() {
    return this.handlereq1();
  }

  handlereq22017() {
    fetch(
      "http://localhost:8000/query3_direktkandidaten2017/" +
        this.state.value.toString()
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("p");
        var tag_id = document.getElementById("direktkand2017");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }
  renderTable22017() {
    return this.handlereq22017();
  }

  handlereq2() {
    fetch(
      "http://localhost:8000/query3_direktkandidaten/" +
        this.state.value.toString()
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("p");
        var tag_id = document.getElementById("direktkand");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }
  renderTable2() {
    return this.handlereq2();
  }

  handlereq3() {
    fetch(
      "http://localhost:8000/query3_stimmen_entwicklung/" +
        this.state.value.toString()
    )
      .then(function (response) {
        return response.json();
      })
      .then(function (data) {
        // const newContent = document.createElement("table");
        var tag_id = document.getElementById("p_entw");
        tag_id.innerHTML = data["data"];
        return data["data"];
      })
      .catch(function (err) {
        console.log("Fetch Error :-S", err);
      });
  }
  renderTable3() {
    this.handlereq3();
  }
}

export default WahlkreisZweit;
