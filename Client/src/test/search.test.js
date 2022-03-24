import React from 'react';
import Search from '../components/search';
import Enzyme, { shallow, render, mount } from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';

const baseProps = {handle : null, updateMain : null, defaultError : null};

Enzyme.configure({ adapter: new Adapter() });
const wrapper = mount(<Search {...baseProps} />, { attachTo: document.body }).instance();


describe("Update tests", () => {
    test('Field changes', () => {
        wrapper.onSearchTypeChange({target : {value : 'category'}});
        wrapper.onSearchTextChange({target : {value : 'business'}});

        expect(wrapper.state.userSearchType).toBe('category');
        expect(wrapper.state.userSearchText).toBe('business');
    });

    test('Add item', () => {
        wrapper.validateForm();
        expect(wrapper.state.criteria.size).toBe(1);
        expect(wrapper.state.userSearchType).toBe(null);
        expect(wrapper.state.userSearchText).toBe(null);
    });

    test('Form reset', () => {
        wrapper.resetCriteria();
        expect(wrapper.state.criteria.size).toBe(0);
        expect(wrapper.state.userSearchType).toBe(null);
        expect(wrapper.state.userSearchText).toBe(null);
    });
})