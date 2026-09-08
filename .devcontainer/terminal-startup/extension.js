const vscode = require('vscode');

async function focusLab() {
  if (!vscode.workspace.workspaceFolders?.length) return;

  // Close views without discarding unsaved files. Use the workbench's terminal
  // service, which owns restored sessions, instead of racing extension-host
  // terminal events or creating a second shell during reconnect.
  for (const command of [
    'workbench.action.closeAllEditors',
    'workbench.action.closeSidebar',
    'workbench.action.closeAuxiliaryBar',
    'workbench.action.positionPanelBottom',
    'workbench.action.alignPanelCenter',
    'workbench.action.closePanel',
    'workbench.action.toggleMaximizedPanel',
    'workbench.action.terminal.focus'
  ]) await vscode.commands.executeCommand(command);
}

function activate(context) {
  context.subscriptions.push(vscode.commands.registerCommand('terminalLab.focus', focusLab));
  return focusLab().catch(error => {
    vscode.window.showErrorMessage(`Lab terminal startup: ${error.message}`);
  });
}

module.exports = { activate };
