const WebSocket = require('ws')
const uuid = require('uuid')        // For later use
const fs = require('fs')

// Create a new websocket server on port 3000
console.log('Ready. On MineCraft chat, type /connect localhost:3000')
const wss = new WebSocket.Server({ port: 3000 })


const first_x = 0
const first_y = 0
const first_z = 1

// const height = 18
// const width = 24
// const width = 128
// const height = 75

const sleep = msec => new Promise(resolve => setTimeout(resolve, msec));


// On Minecraft, when you type "/connect localhost:3000" it creates a connection
wss.on('connection', socket => {
  console.log('Connected')
  socket.send(JSON.stringify({
    "header": {
      "version": 1,                     // We're using the version 1 message protocol
      "requestId": uuid.v4(),           // A unique ID for the request
      "messageType": "commandRequest",  // This is a request ...
      "messagePurpose": "subscribe"     // ... to subscribe to ...
    },
    "body": {
      "eventName": "PlayerMessage"      // ... all player messages.
    },
  }))
  socket.send(JSON.stringify({
    "header": {
      "version": 1,
      "requestId": uuid.v4(),
      "messageType": "commandRequest",
      "messagePurpose": "subscribe"
    },
    "body": {
      "eventName": "PlayerTransform"
    },
  }))

//   socket.on('message', packet => {
//     const msg = JSON.parse(packet)
//     console.log(msg)
//   })
  socket.on('message', async packet => {
      async function send(cmd) {
          const msg = {
            "header": {
              "version": 1,
              "requestId": uuid.v4(),     // Send unique ID each time
              "messagePurpose": "commandRequest",
              "messageType": "commandRequest"
            },
            "body": {
              "version": 1,               // TODO: Needed?
              "commandLine": cmd,         // Define the command
              "origin": {
                "type": "player"          // Message comes from player
              }
            }
          }
          return await new Promise((resolve, reject) => {
            socket.send(JSON.stringify(msg))  // Send the JSON string
            resolve()
            }).then(()=>{
              return
            })
          
      }

      const msg = JSON.parse(packet)
      // If this is a chat window
      if (msg.header.eventName === 'PlayerMessage') {
        const [command, ...args] = msg.body.message.split(' ')

        if(command == "img"){
            // send(`execute @e[name=display] ~ ~ ~ fill ~${first_x} ~${first_y} ~${first_z} ~${first_x+width} ~${first_y+height} ~${first_z} concrete 15`)
          //   for(let y = 0; y < height; y++){//画面初期化
          //     await sleep(0.000001)d
          //     for(let x = 0; x < width; x++){
          //       await sleep(0.000001)
          //       await send(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} concrete 15`)
          //     }
          //   }
          console.log("go!")
          send(`say Start ImageCreater!! Create BY kuwa.dev`)
          const path = `${args[0]}.json`
          try {
            send(`say 画像ファイルを読み込み中...`)
            fs.statSync(path)
          } catch (error) {
            if (error.code === 'ENOENT') {
              console.log(`not found file ${args[0]}.json`)
              send(`say 画像ファイルが見つかりませんでした => ${args[0]}`)
              return
            } else {
              console.log(error)
              send(`say ファイルをチェック中にエラーが発生しました`)
              return
            }
          }
          send(`say ドットを生成中...`)
          let blockList = JSON.parse(fs.readFileSync(path, 'utf8'));
          send('summon armor_stand ~ ~ ~ a display')
          if (args[1] == 'x') {
            send(`execute @e[name=display] ~ ~ ~ fill ~ ~-1 ~ ~${blockList[0].length} ~-1 ~`)
          }else if (args[1] == 'z') {
            send(`execute @e[name=display] ~ ~ ~ fill ~ ~-1 ~ ~ ~-1 ~${blockList[0].length}`)
          }
          
          console.log(blockList.length)
          for(let y = 0; y < blockList.length; y++){
            console.log("complete y:"+y)
            for(let x = 0; x < blockList[y].length; x++){
              if (args[1] == 'x') {
                send(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ${blockList[y][x]}`)
              }else if (args[1] == 'z') {
                send(`execute @e[name=display] ~ ~ ~ setblock ~${first_x} ~${y+first_y} ~${x+first_z} ${blockList[y][x]}`)
              }
              
                
              // console.log(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ${blockList[y][x]}`)
              await sleep(0.00001)
            }
          }
          send(`say ドットが生成されました！`)
          send(`kill @e[name=display]`)



          //   for(let frameNum = 0; frameNum < Object.keys(display).length; frameNum++){
          //     console.log(frameNum)
          //         // await sleep(1)
          //         let y_=height-1
          //         let x_=width-1
          //         for(let y = 0; y < height; y++){
          //             // await sleep(1)
          //           for(let x = 0; x < width; x++){
          //             // console.log(display[frameNum][y][x])
          //               // await sleep(5)
          //               // send(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ${display[y][x]} ${type}`)
          //             if(display[frameNum-1 == -1 ? 1 : frameNum-1][y_][x] == display[frameNum][y_][x]){
          //               continue
          //             }else{
          //               await sleep(0.000001)
          //               await send(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ${display[frameNum][y_][x] == 1?"concrete":"concrete 15"}`)
          //             }
                      
          //               // console.log(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ???? ${type}`)
          //             x_--
          //           }
          //           y_--
          //         }
          //     }

          
        }else if(command == "imgz"){
          // send(`execute @e[name=display] ~ ~ ~ fill ~${first_x} ~${first_y} ~${first_z} ~${first_x+width} ~${first_y+height} ~${first_z} concrete 15`)
        //   for(let y = 0; y < height; y++){//画面初期化
        //     await sleep(0.000001)d
        //     for(let x = 0; x < width; x++){
        //       await sleep(0.000001)
        //       await send(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} concrete 15`)
        //     }
        //   }
        console.log("go!")
        let blockList = JSON.parse(fs.readFileSync("./out.json", 'utf8'));
        console.log(blockList.length)
        for(let y = 0; y < blockList.length; y++){
          console.log("complete y:"+y)
          for(let x = 0; x < blockList[y].length; x++){
              send(`execute @e[name=display] ~ ~ ~ setblock ~${first_x} ~${y+first_y} ~${x+first_z} ${blockList[y][x]}`)
              
              // console.log(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ${blockList[y][x]}`)
              await sleep(0.00001)
          }
        }
        send(`kill @e[name=display]`)



        //   for(let frameNum = 0; frameNum < Object.keys(display).length; frameNum++){
        //     console.log(frameNum)
        //         // await sleep(1)
        //         let y_=height-1
        //         let x_=width-1
        //         for(let y = 0; y < height; y++){
        //             // await sleep(1)
        //           for(let x = 0; x < width; x++){
        //             // console.log(display[frameNum][y][x])
        //               // await sleep(5)
        //               // send(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ${display[y][x]} ${type}`)
        //             if(display[frameNum-1 == -1 ? 1 : frameNum-1][y_][x] == display[frameNum][y_][x]){
        //               continue
        //             }else{
        //               await sleep(0.000001)
        //               await send(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ${display[frameNum][y_][x] == 1?"concrete":"concrete 15"}`)
        //             }
                    
        //               // console.log(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ???? ${type}`)
        //             x_--
        //           }
        //           y_--
        //         }
        //     }

        
      }else if(command == "3dimg"){
          console.log("go!")
          let blockList = JSON.parse(fs.readFileSync("./out.json", 'utf8'));
          console.log(blockList.length)
          for(let y = 0; y < blockList.length; y++){
            console.log("complete y:"+y)
            for(let x = 0; x < blockList[y].length; x++){
                send(`execute @e[name=display] ~ ~ ~ setblock ~${first_x} ~${y+first_y} ~${x+first_z} ${blockList[y][x]}`)
                await sleep(0.000001)
                send(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ${blockList[y][x]}`)
                await sleep(0.000001)
                send(`execute @e[name=display] ~ ~ ~ setblock ~${blockList[y].length+first_x} ~${y+first_y} ~${x+first_z} ${blockList[y][x]}`)
                await sleep(0.000001)
                send(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${blockList[y].length+first_z} ${blockList[y][x]}`)
                // console.log(`execute @e[name=display] ~ ~ ~ setblock ~${x+first_x} ~${y+first_y} ~${first_z} ${blockList[y][x]}`)
                await sleep(0.000001)
            }
          }
          send(`kill @e[name=display]`)

        }else if(msg.body.message == "mapimg"){
          console.log("go!")
          let blockList = JSON.parse(fs.readFileSync("./out.json", 'utf8'));
          console.log(blockList.length)
          for(let y = 0; y < blockList.length; y++){
            console.log("complete y:"+y)
            for(let x = 0; x < blockList[y].length; x++){
                send(`execute @e[name=display] ~ ~ ~ setblock ~${first_x+x} ~${first_y} ~${first_z-y} ${blockList[y][x]}`)
                await sleep(0.000001)
            }
          }
          send(`kill @e[name=display]`)
        }
      }
      
  })
})

