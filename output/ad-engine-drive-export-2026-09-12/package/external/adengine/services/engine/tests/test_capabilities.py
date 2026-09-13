"""Agent discovery and the executable edit-plan completion contract."""
import asyncio

import pytest

from adengine.core import capabilities
from adengine.core.errors import NotFound
from adengine.dr import server as dr
from adengine.gen import server as gen
from adengine import playbooks
from adengine.engines import watch


def test_analysis_capability_is_discoverable_from_both_servers():
    expected = capabilities.get_capability('video-edit-analysis')
    for server in (dr, gen):
        tool_names = {tool.name for tool in asyncio.run(server.mcp.list_tools())}
        assert {'list_agent_capabilities', 'get_agent_capability'} <= tool_names
        assert server.get_agent_capability('video-edit-analysis') == expected
        assert expected in server.list_agent_capabilities('analysis_agent')
        assert expected in server.list_agent_capabilities('editing_agent')
        assert server.list_agent_capabilities('unrelated_agent') == []
    assert expected['owner_agent'] == 'analysis_agent'
    assert expected['handoff_agent'] == 'editing_agent'
    assert expected['visual_analysis']['model'] == watch.gemini_model() == 'gemini-3.8-flash'
    assert expected['visual_analysis']['fallback_allowed'] is False
    assert set(expected['analysis_dimensions']) == {'rushes', 'cuts', 'transitions', 'pacing', 'animations'}
    assert expected['completion']['artifact_kind'] == 'edit_plan'
    assert expected['completion']['status'] == 'ready_for_editor'
    assert 'scene descriptions' in expected['completion']['insufficient_outputs']


def test_capability_workflow_resolves_to_real_tools_and_playbook():
    capability = capabilities.get_capability('video-edit-analysis')
    for stage in capability['workflow']:
        for tool in stage['tools']:
            assert callable(getattr(gen, tool)), tool
    assert playbooks.read(capability['playbook'])
    assert gen.get_edit_plan_contract()['capability_id'] == capability['id']
    assert 'video-edit-analysis' in dr.pipeline_guide()
    assert 'video-edit-analysis' in gen.INSTRUCTIONS
    with pytest.raises(NotFound): capabilities.get_capability('../unknown')
