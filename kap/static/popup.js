function openPopup(discussionId) {
    fetch(`/diskusi/komentar/${discussionId}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById('popup-body').innerHTML = data;
            document.getElementById('popup').style.display = 'block';
            history.pushState(null, '', `/diskusi/${discussionId}`);
        });
}

function closePopup() {
    document.getElementById('popup').style.display = 'none';
    history.pushState(null, '', '/diskusi');
}

function submitComment() {
    console.log('submitting comment');
      // fetch post
      const form = document.getElementById("comment-form");
      const formData = new FormData(form);
      try {
        fetch(`/diskusi/komentar/${formData.get("discussion_id")}/`, {
          method: "POST",
          headers: {
            "X-CSRFToken": "{{ csrf_token }}",
          },
          body: formData,
        })
          .then((response) => {
            if (!response.ok) {
              throw new Error("Network response was not ok");
            }
            return response.text();
          })
          .then((data) => {
            document.getElementById("popup-body").innerHTML = data;
          })
          .catch((error) => {
            window.alert(
              "An error occurred while submitting your comment. Please try again."
            );
            console.error("Error:", error);
          });
      } catch (error) {
        window.alert(
          "An error occurred while submitting your comment. Please try again."
        );
        console.error("Error:", error);
      }
    }
