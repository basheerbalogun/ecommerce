let btns = document.getElementsByClassName('addtocart')
for (let i = 0; i < btns.length; i++){
    btns[i].addEventListener('click', function (e){
      let item_id = e.target.dataset.item
      let action = e.target.dataset.action
      console.log(item_id)
      if(user=='AnonymousUser'){
         console.log('You are not signed in')
      }
      else{
          addtocart(item_id, action)
      }
    })
}

function addtocart(i_id, act){
    const data = { item_id: i_id, action:act };

let url = '/update-cart'
fetch('url', {
  method: 'POST', // or 'PUT'
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
})
  .then((response) => response.json())
  .then((data) => {
    console.log('Success:', data);
  })
  .catch((error) => {
    console.error('Error:', error);
  });
}