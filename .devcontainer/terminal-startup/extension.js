const vscode = require('vscode');

async function focusLab() {
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder) return;

  // Reuse the student's terminal on reconnect. Never reset their shell or files.
  const terminal = vscode.window.terminals.find(t => t.name === 'Lab 1 - Bash')
    || vscode.window.createTerminal({
      name: 'Lab 1 - Bash',
      shellPath: '/bin/bash',
      cwd: folder.uri.fsPath,
      location: vscode.TerminalLocation.Panel
    });

  // These close views, not documents on disk. Unsaved editors retain VS Code's
  // normal save confirmation. No commands or solutions are typed into the shell.
  for (const command of [
    'workbench.action.closeAllEditors',
    'workbench.action.closeSidebar',
    'workbench.action.closeAuxiliaryBar',
    'workbench.action.positionPanelBottom',
    'workbench.action.alignPanelCenter',
    'workbench.action.closePanel',
    'workbench.action.toggleMaximizedPanel'
  ]) await vscode.commands.executeCommand(command);
  terminal.show(false);
  await vscode.commands.executeCommand('workbench.action.terminal.focus');
}

function activate(context) {
  context.subscriptions.push(vscode.commands.registerCommand('terminalLab.focus', focusLab));
  return focusLab().catch(error => {
    vscode.window.showErrorMessage(`Lab terminal startup: ${error.message}`);
  });
}

module.exports = { activate };
