var attack_from = -1;
var move_done = false; // to avoid multiple moves in submit timeout

function isDone(){
    if(document.getElementsByName('v0')[0].value == "0" &&
       document.getElementsByName('v1')[0].value == "0"){
       return true;
    }
    if(document.getElementsByName('v2')[0].value == "0" &&
       document.getElementsByName('v3')[0].value == "0"){
       return true;
    }
    return false;
}

function updateVisibility(){
    for (elm_name of ['0', '1', '2', '3']) {
        var elm = document.getElementById(elm_name);
        if(elm.innerHTML == "0"){
            elm.style.visibility = "hidden";
        } else {
            elm.style.visibility = "visible";
        }
    }
}

function SubmitTheForm(){
    document.getElementById('myform').submit();
}
    
function Restart(){
    for (elm of ['v0', 'v1', 'v2', 'v3']) {
        document.getElementsByName(elm)[0].value = "1";
    }
    SubmitTheForm();
}
    
function SelectOrUnSelect(x) {
    updateVisibility();
    if (move_done){
        return;
    }
    if (x.className == 'hand notselected'){
        if ((x.id == '2' || x.id == '3') && (attack_from == -1)) {
            // choose where to attack from
            if (1 * (x.innerHTML) != 0){
                attack_from = x.id;
                x.className = 'hand selected';
                markSelectHandTo();
            }
        } else if (attack_from.value != -1){
            // choose where to attack
            if (1 * x.innerHTML != 0){
                attack_from_element = document.getElementById(attack_from);
                attack_from_element.className = 'hand notselected';
                x.innerHTML = ( (1*(attack_from_element.innerHTML) + (1*x.innerHTML)) % 5 );
                document.getElementsByName('v' + x.id)[0].value = x.innerHTML
                submitWithDelay();
            }
        }   
    } else {
        attack_from = -1;
        x.className = 'hand notselected';
        markSelectHandFrom();
    }
}


function markSelectHandFrom(){
    if(!isDone()){
        document.getElementById('instruction').innerHTML = "Your turn: Choose hand to attack from";
    }
}


function markSelectHandTo(){
    if(!isDone()){
        document.getElementById('instruction').innerHTML = "Your turn: Choose which hand to attack";
        // TODO "or split" if applicable
    }
}


function submitWithDelay(){
    mark_done = true;
    setTimeout(SubmitTheForm, 1000);
    updateVisibility();
    document.getElementById('instruction').innerHTML = "Thinking...";
}


function SelectSplit(){
    if (move_done){
        return;
    }
    split_it = document.getElementById(attack_from);
    another = document.getElementById(5 - split_it.id);
    if (((1 * split_it.innerHTML) % 2 == 0) && (1*another.innerHTML == 0)){
        // split is valid
        val = 1*split_it.innerHTML / 2;
        another.innerHTML = val;
        split_it.innerHTML = val;
        document.getElementsByName('v2')[0].value = val;
        document.getElementsByName('v3')[0].value = val;
        split_it.className = 'hand notselected';
        submitWithDelay();
        //markSelectHandFrom()
    }
}

