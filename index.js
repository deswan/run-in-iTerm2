#!/usr/bin/env node


var inquirer = require("inquirer");
var cp = require("child_process");
const {read} = require("node-yaml")
const path = require("path")
const os = require("os")
const configFilePath = path.join(os.homedir(), '.run-in-iterm2.yaml')


function formatCommand(command){
    if(typeof command === 'string'){
        return [command]
    }else{
        return command
    }
}

async function main(){
    let { defaultPath, defaultCommand, projects } = await read(configFilePath)
    projects = projects.map(project => {
        if(typeof project === 'string'){
            project =  {
                name: project,
                title: project,
            }
        }else if(!project.title){
            project = {
                ...project,
                title: project.name
            }
        }

        
        project = {
            command: defaultCommand,
            path: path.join(defaultPath, project.name),
            ...project
        }

        project.command = formatCommand(project.command)

        return project
    })

    inquirer
        .prompt([
            {
                type: "list",
                name: "project",
                message: "请选择项目",
                choices: projects.map(e => ({
                    name: e.name,
                    value: e,
                }))
            }
        ])
        .then(answers => {
            cp.exec("open /Applications/iTerm.app", (error, stdout, stderr) => {
                if (!error) {
                    let { project } = answers;
                    let job = cp.spawn("python3", [
                        "/Users/futunn/run_futu/run.py",
                        project.title,
                        project.path,
                        ...project.command
                    ]);
                    job.stdout.on("data", data => {
                        console.log(`${data}`);
                    });
            
                    job.stderr.on("data", data => {
                        console.error(`${data}`);
                    });
            
                    job.on("close", code => {
                        if(!code){
                            console.log(`🎈 run success 🎈`);
                        }else{
                            console.error(`run failed!`);
                        }
                    });
                }
            });
        });
}


main()