
const codeBox = document.querySelector('#codeBox')
console.log(codeBox)

// not editable
const editor = ace.edit(codeBox, {
  theme: 'ace/theme/Berlin',
  mode: 'ace/mode/python',
  fontSize: 16,
  showPrintMargin: false,
  fontFamily: 'monospace',
  fontWeight: 'bold',
  highlightActiveLine: true

})

// enable input and button
function enableInput () {
  const promptInput = document.querySelector('#promptInput')
  promptInput.disabled = false

  const sendButton = document.querySelector('.submit')
  sendButton.disabled = false
}

function sendApiRequest (params) {
  const promptInput = document.querySelector('#promptInput')
  // disable input
  promptInput.disabled = true
  
  const sendButton = document.querySelector('.submit')
  // disable button
  sendButton.disabled = true
  editor.setValue('Loading...')
  // send request to api
  fetch(`http://localhost:5000/generate_code?query=${params}`)
    .then(response => response.json())
    .then(data => {
      console.log('Success:', data)
      document.querySelector('img').src = ''

      // update linter
      editor.setValue(data.code)
      console.log(data.plot)
      document.querySelector('img').src = data.plot
      enableInput()
    })
}

// bind text area with id promptInput to enter key to make a console log
const promptInput = document.querySelector('#promptInput')
promptInput.addEventListener('keyup', function (e) {
  if (e.key === 'Enter') {
    sendApiRequest(promptInput.value)
  }
})

const sendButton = document.querySelector('.submit')
sendButton.addEventListener('click', function (e) {
  sendApiRequest(promptInput.value)
})
// Can you select 'Sex' column and make a plot them with a pie chart and replace the axis labels with 'men' and 'woman' respectively