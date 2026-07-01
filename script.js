// ===============================
// Compiler Front-End Dashboard
// ===============================

async function compileCode() {

    const code = document.getElementById("code").value;

    const response = await fetch("/compile", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            code: code
        })

    });

    const data = await response.json();

    updateStatistics(data.statistics);

    updatePhases(data.phases);

    updateTokens(data.tokens);

    updateSymbols(data.symbol_table);

    updateConsole(data.console);

    drawTree(data.ast);

}

// ===============================
// CLEAR EDITOR
// ===============================

function clearEditor(){

    document.getElementById("code").value="";

    document.getElementById("tokenTable").innerHTML="";

    document.getElementById("symbolTable").innerHTML="";

    document.getElementById("console").innerHTML="Waiting for compilation...";

    d3.select("#treeSvg").selectAll("*").remove();

}

// ===============================
// DOWNLOAD REPORT
// ===============================

function downloadReport(){

    const content=document.getElementById("console").innerText;

    const blob=new Blob([content],{

        type:"text/plain"

    });

    const link=document.createElement("a");

    link.href=URL.createObjectURL(blob);

    link.download="compiler_report.txt";

    link.click();

}

// ===============================
// STATISTICS
// ===============================

function updateStatistics(stats){

    document.getElementById("totalTokens").innerText=stats.tokens;

    document.getElementById("identifiers").innerText=stats.identifiers;

    document.getElementById("operators").innerText=stats.operators;

    document.getElementById("errors").innerText=stats.errors;

}
// ===============================
// COMPILER PHASES
// ===============================

function updatePhases(phases){

    const container=document.getElementById("phases");

    container.innerHTML="";

    for(const phase in phases){

        const status=phases[phase];

        const card=document.createElement("div");

        card.className="phase";

        card.innerHTML=`

            <h3>${phase}</h3>

            <p class="${status==="Completed" ? "success" : "failed"}">

                ${status}

            </p>

        `;

        container.appendChild(card);

    }

}

// ===============================
// TOKEN TABLE
// ===============================

function updateTokens(tokens){

    const table=document.getElementById("tokenTable");

    table.innerHTML="";

    tokens.forEach((token,index)=>{

        table.innerHTML+=`

        <tr>

            <td>${index+1}</td>

            <td>${token.type}</td>

            <td>${token.value}</td>

        </tr>

        `;

    });

}

// ===============================
// SYMBOL TABLE
// ===============================

function updateSymbols(symbols){

    const table=document.getElementById("symbolTable");

    table.innerHTML="";

    symbols.forEach(symbol=>{

        table.innerHTML+=`

        <tr>

            <td>${symbol.identifier}</td>

            <td>${symbol.type}</td>

            <td>${symbol.value}</td>

            <td>${symbol.scope}</td>

        </tr>

        `;

    });

}

// ===============================
// CONSOLE
// ===============================

function updateConsole(messages){

    document.getElementById("console").innerHTML=messages.join("<br>");

}
// ===============================
// AST TREE (D3)
// ===============================

function drawTree(treeData){

    d3.select("#treeSvg").selectAll("*").remove();

    const width=document.getElementById("treeContainer").clientWidth;

    const height=650;

    const svg=d3.select("#treeSvg")
        .attr("width",width)
        .attr("height",height);

    const g=svg.append("g");

    svg.call(

        d3.zoom()

        .scaleExtent([0.5,3])

        .on("zoom",(event)=>{

            g.attr("transform",event.transform);

        })

    );

    const root=d3.hierarchy(treeData);

    const tree=d3.tree()

        .size([width-200,height-120]);

    tree(root);

    // -------- LINKS --------

    g.selectAll(".link")

        .data(root.links())

        .enter()

        .append("line")

        .attr("class","link")

        .attr("x1",d=>d.source.x+100)

        .attr("y1",d=>d.source.y+40)

        .attr("x2",d=>d.target.x+100)

        .attr("y2",d=>d.target.y+40);

    // -------- NODES --------

    const node=g.selectAll(".node")

        .data(root.descendants())

        .enter()

        .append("g")

        .attr("class","node")

        .attr("transform",d=>

            `translate(${d.x+100},${d.y+40})`

        );

    node.append("circle")

        .attr("r",18);

    node.append("text")

        .attr("dy",5)

        .attr("text-anchor","middle")

        .text(d=>d.data.name);

}

// ===============================
// PAGE LOADED
// ===============================

window.onload=function(){

    document.getElementById("console").innerHTML=
        "Ready for Compilation...";

}