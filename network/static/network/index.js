document.addEventListener('DOMContentLoaded', function(){   
    try {
        document.getElementById("new-post").addEventListener("click", showPostArea);  
        document.getElementById("post-submit").addEventListener("click", submitPost);
    } catch (error) {
        console.log(error)
        return
    }
})

function showPostArea (){
    const text_area_div = document.getElementById("post-area-div")
    if(text_area_div.style.display === "block"){
        text_area_div.style.display ="none";    
    }
    else{
        text_area_div.style.display ="block"
    }
}

function submitPost(){
    const text_area_div = document.getElementById("post-area-div")
    const post_value = document.getElementById("post-area");
    const token = getCookie("csrftoken")
    console.log(post_value.value)

    fetch("/newPost",{
        headers :{"X-CSRFToken":token},
        method: "POST",
        mode: "same-origin",
        body: JSON.stringify({
            body: post_value.value,
        })
    }).then(response => response.json())
    .then(result => {
        console.log(result)
        get_post_by_id(result.message)
    })

    //end function resetting textarea empty
    post_value.value ="";
    text_area_div.style.display ="none"

    
}

function get_post_by_id(id){

    const newPost_div = document.getElementById("new-post-div");

    fetch(`/post/${id}`).then(response => response.json())
    .then(result => {
        console.log(result)

        // outer divs
        const userRow = document.createElement("div");
        const bodyRow = document.createElement("div");
        const footerRow = document.createElement("div");
        const likeDiv = document.createElement("div");
        
        // contents
        const user_anchor = document.createElement("a");
        const body_div = document.createElement("div")
        const numLike_span =document.createElement("span");
        const like_span = document.createElement("span");
        const date_span = document.createElement("span");
        
        // class row assignet to outer divs
        userRow.className ="row";
        bodyRow.className = "row pb-3";
        footerRow.className ="row";
        likeDiv.className ="col-3";
        
        // contents style assigned via bootsrap
        user_anchor.href = `/profiles/${result.creator}`
        user_anchor.className = "col-12";
        body_div.className ="col-12";
        numLike_span.className ="m-1";
        numLike_span.id = `${id}`;
        like_span.className ="cursor";
        date_span.className ="col-9";
        
        // assigne html values to contents
        user_anchor.innerHTML = `<div><h5>${result.creator}</h5></div>`;
        body_div.innerHTML = result.body;
        numLike_span.innerHTML = getLikes(id);
        like_span.innerHTML = "&#128077;";
        date_span.innerHTML = result.date;
        
        // append contents to outer divs
        userRow.appendChild(user_anchor);
        bodyRow.append(body_div);
        
        // append likes to like div
        likeDiv.append(numLike_span,like_span);
        
        // append like div and date_span to footer row
        footerRow.append(likeDiv,date_span);
        
        // append outer divs to newPostDiv
        newPost_div.prepend(userRow,bodyRow,footerRow);

        newPost_div.style.display = "block";
        like_span.addEventListener("click",() => like(id));

    })
    newPost_div.style.animationPlayState = "running" 
}

function editPost(post_id){
    
    const bodyRow = document.getElementById(`body-${post_id}`)
    const body = document.getElementById(`body-post${post_id}`)
    const bodyValue = body.innerHTML
    const editArea = document.createElement("textarea")
    const layout_span = document.createElement("span");
    layout_span.className ="col-2"
    editArea.value = bodyValue
    const saveBtn = document.createElement("button")
    saveBtn.innerHTML ="Save"
    saveBtn.className = "btn btn-outline-primary ml-3 mb-1 col-2"
    Object.assign(editArea, {
        className:"col-9 ml-3 mb-1 mt-1 p-0",
        cols:"70",
        rows:"6",
    })
    body.style.display="none"
    bodyRow.append(editArea, layout_span,saveBtn)

    saveBtn.addEventListener("click", ()=>{
        const token = getCookie("csrftoken")

        fetch("/edit",{
            headers :{"X-CSRFToken":token},
            method:"PUT",
            mode: "same-origin",
            body: JSON.stringify({
                id:post_id,
                body : editArea.value,
            })
        }).then(response => response.json())
        .then(result => {
            console.log(result)
            body.innerHTML = editArea.value
            bodyRow.removeChild(editArea)
            bodyRow.removeChild(layout_span)
            bodyRow.removeChild(saveBtn)
            body.style.display = "block"
        })
    })

    console.log(bodyValue)
    
}

function deletePost(post_id){
    const bodyRow = document.getElementById(post_id)

    const token = getCookie("csrftoken")

    fetch("/edit",{
        headers :{"X-CSRFToken":token},
        method:"DELETE",
        mode: "same-origin",
        body: JSON.stringify({
            id:post_id,
        })
    }).then(response=> response.json())
    .then(result => {
        console.log(result)
    })

    bodyRow.remove()
    console.log(bodyRow)
}

function like(post_id){

    const token = getCookie("csrftoken")
    const likes = document.getElementById(post_id)
    fetch(`/like/${post_id}`,{
        headers :{"X-CSRFToken":token},
        method:"POST",
        mode: "same-origin",
        body: JSON.stringify({
            like: true,
        })
    }).then(response => response.json())
    .then(result => {
        console.log(result)
        likes.innerHTML = parseInt(likes.innerHTML) + result.likes
    })
    
}

function getLikes(post_id){
    let numLike= 0
    fetch(`/like/${post_id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);
        numLike = result.results;
    })
    return numLike
}

function follow(user_id){
    const token = getCookie("csrftoken");

    fetch(`/follow/${user_id}`, {
        headers : {"X-CSRFToken":token},
        method : "POST",
        mode : "same-origin",
        body : JSON.stringify({
            follow: true,
        })
    }).then(response => response.json())
    .then(result => {
        console.log(result)
        const followers = document.getElementById("followers")
        const button = document.getElementById(user_id)
        if (result.follow === true){
            followers.innerHTML = parseInt(followers.innerHTML) + 1;
            button.innerHTML = "Unfollow";
        } 
        else{
            followers.innerHTML = parseInt(followers.innerHTML) - 1;
            button.innerHTML = "Follow"
        }
    })
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}