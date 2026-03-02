/**
 * Tests for the editor store
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { useEditorStore } from './editorStore';

describe('editorStore', () => {
  beforeEach(() => {
    // Reset the store before each test
    useEditorStore.setState({
      inputContent: '',
      outputContent: '',
      errors: [],
      warnings: [],
      isConverting: false,
    });
  });

  it('should have initial state', () => {
    const state = useEditorStore.getState();
    expect(state.delimiter).toBeDefined();
    expect(state.outputFormat).toBeDefined();
  });

  it('should update input content', () => {
    const { setInputContent } = useEditorStore.getState();
    setInputContent('test content');

    const state = useEditorStore.getState();
    expect(state.inputContent).toBe('test content');
  });

  it('should update delimiter', () => {
    const { setDelimiter } = useEditorStore.getState();
    setDelimiter('|');

    const state = useEditorStore.getState();
    expect(state.delimiter).toBe('|');
  });

  it('should update output format', () => {
    const { setOutputFormat } = useEditorStore.getState();
    setOutputFormat('shex');

    const state = useEditorStore.getState();
    expect(state.outputFormat).toBe('shex');
  });

  it('should toggle skip header', () => {
    const initialState = useEditorStore.getState();
    const initialSkipHeader = initialState.skipHeader;

    const { setSkipHeader } = useEditorStore.getState();
    setSkipHeader(!initialSkipHeader);

    const state = useEditorStore.getState();
    expect(state.skipHeader).toBe(!initialSkipHeader);
  });

  it('should set output content', () => {
    const { setOutputContent } = useEditorStore.getState();
    setOutputContent('output result');

    const state = useEditorStore.getState();
    expect(state.outputContent).toBe('output result');
  });

  it('should set errors', () => {
    const { setErrors } = useEditorStore.getState();
    const testErrors = [{ line: 1, column: null, message: 'Test error', source_line: null }];
    setErrors(testErrors);

    const state = useEditorStore.getState();
    expect(state.errors).toEqual(testErrors);
  });

  it('should set converting state', () => {
    const { setIsConverting } = useEditorStore.getState();
    setIsConverting(true);

    const state = useEditorStore.getState();
    expect(state.isConverting).toBe(true);
  });
});
