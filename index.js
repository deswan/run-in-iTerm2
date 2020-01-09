var inquirer = require("inquirer");
var cp = require("child_process");
inquirer
    .prompt([
        {
            type: "list",
            name: "path",
            message: "请选择项目",
            choices: [
                {
                    name: "futu5_ipo",
                    value: ["futu5_ipo", "/Users/futunn/futu5_ipo"]
                }
            ]
        }
    ])
    .then(answers => {
        cp.exec("open /Applications/iTerm.app", (error, stdout, stderr) => {
            console.log(stdout);
            console.error(stderr);
            if (!error) {
                let { path } = answers;
                let job = cp.spawn("python3", [
                    "/Users/futunn/run_futu/run.py",
                    path[0],
                    path[1]
                ]);
                job.stdout.on("data", data => {
                    console.log(`stdout: ${data}`);
                });
        
                job.stderr.on("data", data => {
                    console.error(`stderr: ${data}`);
                });
        
                job.on("close", code => {
                    console.log(`子进程退出，退出码 ${code}`);
                });
            }
        });
    });
