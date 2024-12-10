import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [playlists, setPlaylists] = useState([])
  useEffect(() => {
    fetch_playlists()
  
  }, [])

  const fetch_playlists = async () => {

    const response = await fetch("http://127.0.0.1:5000/playlists");
    console.log(response);
    const data = await response.json();
    //setPlaylists(data.items)
    console.log(data);
  }
  return (
    <>
      <p>hello</p>

    </>
  )
}

export default App
