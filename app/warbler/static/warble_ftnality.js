"use strict";

const $likesBtn = $(".heart-icon")

const $newMessageLink = $("#new-message")
const $submitMsgBtn = $("#create-msg")
const $newMsgForm = $("#new-message-form")



/** changes like button appearance depending on
 * current like status
*/
async function alterLikeStatus(evt) {
  evt.stopImmediatePropagation();
  console.log(evt)
  const id = $(evt.target).attr("id")
  const resp = await axios.post(`/messages/${id}/like`)

  if (resp.status == 200){
    if($(evt.target).attr("class") === "heart-icon bi bi-heart-fill"){
      $(evt.target).attr("class", "heart-icon bi bi-heart")
    }
    else{
      $(evt.target).attr("class", "heart-icon bi bi-heart-fill")
    }
  }
}


$likesBtn.on("click", alterLikeStatus)
