const vscode = require('vscode');

function restoredLabTerminal() {
  const existing = vscode.window.terminals.find(t => t.name === 'Lab 1 - Bash');
  if (existing) return Promise.resolve(existing);
  // Persistent terminals arrive asynchronously after the extension host starts.
  // Give restoration time to publish the existing shell before creating one.
  return new Promise(resolve => {
    const finish = terminal => {
      clearTimeout(timeout);
      listener.dispose();
      resolve(terminal);
    };
    const listener = vscode.window.onDidOpenTerminal(terminal => {
      if (terminal.name === 'Lab 1 - Bash') finish(terminal);
    });
    const timeout = setTimeout(() => finish(
      vscode.window.terminals.find(t => t.name === 'Lab 1 - Bash')
    ), 5000);
  });
}

async function focusLab(waitForRestore = false) {
  const folder = vscode.workspace.workspaceFolders?.[0];
  if (!folder) return;

  // Reuse the student's terminal on reconnect. Never reset their shell or files.
  const terminal = (waitForRestore ? await restoredLabTerminal()
    : vscode.window.terminals.find(t => t.name === 'Lab 1 - Bash'))
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
  context.subscriptions.push(vscode.commands.registerCommand('terminalLab.focus', () => focusLab()));
  return focusLab(true).catch(error => {
    vscode.window.showErrorMessage(`Lab terminal startup: ${error.message}`);
  });
}

module.exports = { activate };
