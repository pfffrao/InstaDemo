
function error_cb(error) {
    console.log(error);
    console.error(error)
}

/*
 *
 *    Likes
 *
 */

function create_like(success_cb, error_cb) {
    var post_pk = parseInt($(this).siblings('.like-hidden-data').find('.post-pk').html());
    console.log(post_pk);

    $.ajax({
        type: "POST",
        url: '/insta/like',
        data: {
            'post_id': post_pk
        },
        success: function(data) { success_cb(data); },
        error: function(error) { error_cb(error); }
    });
}
  
function like_update_view(data) {
    console.log(data);

    // toggle heart
    var $hiddenData = $('.like-hidden-data.' + data.post_pk);
    if (data.result != 0) {
      $hiddenData.siblings('.submit-like').removeClass('fa-heart-o').addClass('fa-heart');
    }else if(data.result == -1){
      alert('Please login first');
    } 
    else {
      $hiddenData.siblings('.submit-like').removeClass('fa-heart').addClass('fa-heart-o');
    }
  
    // update like count
    var difference = data.result ? 1 : -1;
    var $post = $('.view-update.' + data.post_pk);
    var $likes = $post.find('.likes');
    var likes = parseInt($likes.text());
    likes = likes + difference;
  
    console.log('likes', likes);
  
    if (likes == null || isNaN(likes)) {
      $likes.text('1 like');
    } else if (likes === 0) {
      $likes.text('');
    } else if (likes === 1) {
      $likes.text('1 like');
    } else {
      $likes.text(likes + ' likes');
    }
}
 
$('.submit-like').on('click', function() {
    create_like.call(this, like_update_view, error_cb);
});

  
/*
*
*    Comments
*
*/
  
function enterPressed(e) {
    if (e.key === "Enter") { return true; }
    return false;
}
   
function validComment(text) {
    if (text == '') return false;
    return true;
}
  
function create_comment(success_cb, error_cb) {
    var comment_text = $(this).val();
    var post_pk = $(this).parent().siblings('.hidden-data').find('.post-pk').text();
  
    console.log(comment_text, post_pk);
  
    $.ajax({
      type: "POST",
      url: '/comment',
      data: {
        comment_text: comment_text,
        post_pk: post_pk
      },
      success: function(data) { success_cb(data); },
      error: function(error) { error_cb(error); }
    });
}

function comment_update_view(data) {
    console.log(data);
    var $post = $('.hidden-data.' + data.post_pk);
    var commentHTML = '<li class="comment-list__comment"><a class="user"> ' + data.commenter_info.username + '</a> <span class="comment">'
                    + data.commenter_info.comment_text +'</span></li>'
  
    $post.closest('.view-update').find('.comment-list').append(commentHTML);
  }
  
  $('.add-comment').on('keyup', function(e) {
    if (enterPressed(e)) {
      if (validComment($(this).val())) {
        create_comment.call(this, comment_update_view, error_cb);
        $(this).val('');
      }
    }
  });
  

/*
 *
 *    Follow/Unfollow
 *
 */

// function follow_user(success_cb, error_cb, type) {
//     var follow_user_pk = $(this).attr('id');
//     console.log(follow_user_pk);
  
//     $.ajax({
//       method: "POST",
//       url: '/togglefollow',
//       data: {
//         'follow_user_pk': follow_user_pk,
//         'type': type
//       },
//       success: function(data) { success_cb(data); },
//       error: function(error) { error_cb(error); }
//     });
// }
  
// function update_follow_view(data) {
//     if (data.result == -1){
//       console.log('Please login');
//     }
//     console.log('calling update_follow_view');
//     console.log('data',data);
//     var $button = $('.follow-toggle__container .btn');
//     $button.addClass('unfollow-user').removeClass('follow-user');
//     $button.text('Unfollow');

//     var $span = $('.follower_count');
//     var span_text = parseInt(document.getElementById("follower_id").innerText);
//     $span.text(span_text + 1);
// }

// function update_unfollow_view(data) {
//     console.log('calling update_unfollow_view');
//     console.log('data',data);
//     var $button = $('.follow-toggle__container .btn');
//     $button.addClass('follow-user').removeClass('unfollow-user');
//     $button.text('Follow');

//     var $span = $('.follower_count');
//     var span_text = parseInt(document.getElementById("follower_id").innerText);
//     $span.text(span_text - 1);
// }


// $('.follow-toggle__container').on('click', '.follow-user', function() {
//     follow_user.call(this, update_follow_view, error_cb, 'follow');
// });

// $('.follow-toggle__container').on('click', '.unfollow-user', function() {
//     follow_user.call(this, update_unfollow_view, error_cb, 'unfollow');
// });

// ======================
// my own follow function
// ======================
function createFollow(success_cb, error_cb, type){
  var $userpk = parseInt($('div.follow-toggle__container').find('.user-pk').text())
  $.ajax({
    type:'POST',
    url:'follow',
    data:{
      'followed_pk': $userpk,
      type:type
    },
    success: function (data){success_cb(data);},
    error:  function (data){error_cb(data);},

  })
}

var followingMsgClassName = "following-text";
var unfollowedMsgClassName = "unfollowed-text";

function toggleFollowView(data){
  // update follow text, show is following
  if(data.result == -1){
    console.log('Please login.');
    return;
  }
  // console.log('Toggling follow view...');
  var $followText = $('.unfollowed-text');
  // console.log($followText.html());
  var theText = $followText.html();
  theText = theText.replace(/not/g, "now");
  $followText.html(theText);
  $followText.addClass(followingMsgClassName).removeClass(unfollowedMsgClassName);

  // update follower button
  var $followBtn = $('.follow-user');
  $followBtn.addClass('unfollow-user').removeClass('follow-user');
  $followBtn.text('Unfollow');
  // update profile follower count
  var $followerCnt = $('span.follower__count');
  var spanNum = parseInt($followerCnt.text());
  // console.log(spanNum);

  $followerCnt.text(spanNum + 1);

  // console.log('follow view complete');
}

function toggleUnfollowView(data){
  // update follow text, show is not following
  if(data.result == -1){
    console.log('Please login.');
  }
  // console.log('Toggling follow view...');
  var $followText = $('.following-text');
  // console.log($followText.html());
  var theText = $followText.html();
  theText = theText.replace(/now/g, "not");
  // theText.replace('now', 'not');
  $followText.text(theText);
  $followText.addClass(unfollowedMsgClassName).removeClass(followingMsgClassName);

  // update follower button
  var $followBtn = $('.unfollow-user');
  // console.log($followBtn);
  $followBtn.addClass('follow-user').removeClass('unfollow-user');
  $followBtn.text('Follow');

  // update profile follower count
  var $followerCnt = $('span.follower__count');
  var spanNum = parseInt($followerCnt.text());
  
  // console.log(spanNum);

  $followerCnt.text(spanNum - 1);
  
  // console.log('Unfollow view complete');
}

$('.follow-toggle__container').on('click', '.follow-user' ,function(){createFollow.call(this, toggleFollowView, error_cb, 'follow')});

$('.follow-toggle__container').on('click','.unfollow-user', function(){createFollow.call(this, toggleUnfollowView, error_cb, 'unfollow')})

/*
navbar hover

*/