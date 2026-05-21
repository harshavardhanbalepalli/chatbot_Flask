import { useState } from "react"

function App() {
  const [prompt, setPrompt] = useState("");
  const [history, setHistory] = useState([]);
  const getResponse = async ()=>{
    if(prompt === ""){
      return "please enter the prompt"
    }
    const request = await fetch("http://localhost:8000/chat", {
      method:'POST', 
      headers:{
        "content-type":"application/json"
      },
      body: JSON.stringify({
        "message":prompt
      })
    })
    const response = await request.json();
    setHistory(response.history);
    console.log(response)
  }
  return (
    <>
    <input type="text" 
    placeholder="ask me anything.."
    value={prompt}
    onChange={(e)=>{
      setPrompt(e.target.value)
    }}
    />
    <button onClick={getResponse}>send</button>
    <ul>
      {
          history.map((msg, index)=>{
            return(
            <li key={index}>
              {msg[1]}
            </li>
            )
        })
      }
    </ul>
    
    </>
  )
}

export default App
